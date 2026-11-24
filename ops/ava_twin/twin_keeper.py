#!/usr/bin/env python3
"""AVA Twin Keeper: offline, auditable opportunity memory, no API keys or trades.

A deterministic companion to the existing AVA/Twin/Fuse family, NOT an LLM.
No private data is bundled, no network connection, and no unattended actions.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import sqlite3
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS leads (
 key TEXT PRIMARY KEY,
 title TEXT NOT NULL,
 kind TEXT NOT NULL,
 amount_cents INTEGER NOT NULL,
 restricted INTEGER NOT NULL DEFAULT 0,
 evidence_url TEXT NOT NULL,
 lineage TEXT NOT NULL,
 verified INTEGER NOT NULL DEFAULT 0,
 due_date TEXT,
 effort_minutes INTEGER NOT NULL DEFAULT 15,
 human_gate TEXT NOT NULL DEFAULT '',
 status TEXT NOT NULL DEFAULT 'open',
 created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 lead_key TEXT NOT NULL,
 action TEXT NOT NULL,
 evidence TEXT NOT NULL,
 created_at TEXT NOT NULL,
 FOREIGN KEY(lead_key) REFERENCES leads(key)
);
CREATE INDEX IF NOT EXISTS idx_events_lead ON events(lead_key);
'''

class GuardError(ValueError):
    pass

def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def connect(path):
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript(SCHEMA)
    return con

def canonical_key(obj):
    # Same real source + same underlying program = one lead, not repeated fake consensus.
    lineage = obj.get('lineage', '').strip().lower()
    title = obj.get('title', '').strip().lower()
    if not lineage or not title:
        raise GuardError('title and source lineage required')
    return hashlib.sha256((lineage + '\n' + title).encode()).hexdigest()[:20]

def add(con, item):
    required = ('title', 'kind', 'lineage', 'evidence_url')
    for name in required:
        if not isinstance(item.get(name), str) or not item[name].strip():
            raise GuardError(f'{name} is required')
    if item['kind'] not in ('grant', 'refund', 'service', 'bill', 'job', 'other'):
        raise GuardError('unknown kind')
    amount = item.get('amount_cents', 0)
    if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
        raise GuardError('amount_cents must be a nonnegative integer')
    if not item['evidence_url'].startswith(('https://','http://','local://')):
        raise GuardError('evidence must include a link or local source ref')
    gate = str(item.get('human_gate',''))
    key = canonical_key(item)
    con.execute('''INSERT OR IGNORE INTO leads
       (key,title,kind,amount_cents,restricted,evidence_url,lineage,verified,due_date,effort_minutes,human_gate,created_at)
       VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',
       (key,item['title'].strip(),item['kind'],amount,int(bool(item.get('restricted',False))),
        item['evidence_url'],item['lineage'],int(bool(item.get('verified',False))),
        item.get('due_date'),max(1,int(item.get('effort_minutes',15))),gate,timestamp()))
    added = con.execute('SELECT changes() AS n').fetchone()['n'] > 0
    if added:
        con.execute('INSERT INTO events(lead_key,action,evidence,created_at) VALUES(?,?,?,?)',
                    (key,'recorded','intake only; no cash assumed',timestamp()))
    con.commit()
    return {'id':key,'new':added}

def change_status(con,key,status,evidence=''):
    if status not in ('open','declined','blocked','submitted','accepted','paid','refunded'):
        raise GuardError('unsupported status')
    row=con.execute('SELECT * FROM leads WHERE key=?',(key,)).fetchone()
    if not row:
        raise GuardError('unknown lead id')
    if status in ('paid','refunded'):
        # Fuse proof gate: no 'money received' just because a promotion/offer exists.
        if not row['verified']:
            raise GuardError('proof gate: source not verified')
        if not evidence.strip() or not evidence.startswith(('local://','https://','http://')):
            raise GuardError('proof gate: actual payment or refund receipt reference required')
        if row['restricted']:
            raise GuardError('restricted child/education funds are not spendable cash')
    if status == 'accepted' and not evidence.strip():
        raise GuardError('acceptance needs receipt/reference')
    if status in ('paid', 'refunded'):
        # One payout reference is not two independent payouts. This is a
        # duplicate-proof gate, NOT a bank reconciliation or authenticity check.
        duplicate = con.execute('''SELECT lead_key FROM events
            WHERE action IN ('paid', 'refunded') AND evidence=?
            AND lead_key<>? LIMIT 1''', (evidence, key)).fetchone()
        if duplicate:
            raise GuardError('receipt already used for another lead')
    if row['status'] == status:
        prior = con.execute('''SELECT evidence FROM events
            WHERE lead_key=? AND action=? ORDER BY id DESC LIMIT 1''',
            (key, status)).fetchone()
        if prior and prior['evidence'] == (evidence or 'status only'):
            return  # A repeated CLI call must not create a new payout event.
    con.execute('UPDATE leads SET status=? WHERE key=?',(status,key))
    con.execute('INSERT INTO events(lead_key,action,evidence,created_at) VALUES(?,?,?,?)',
                (key,status,evidence or 'status only',timestamp()))
    con.commit()

def report(con):
    rows=[dict(r) for r in con.execute('SELECT * FROM leads')]
    today=dt.date.today()
    def priority(r):
        due=dt.date.fromisoformat(r['due_date']) if r['due_date'] else None
        urgency=200 if due and due<=today+dt.timedelta(days=2) else 0
        # Favor already verified opportunities with no/minimal human gate; cap speculative $ bait.
        certainty=100 if r['verified'] else -100
        impact=min(150,r['amount_cents']//200)
        gate_penalty=35 if r['human_gate'] else 0
        return urgency+certainty+impact-r['effort_minutes']-gate_penalty
    pending=sorted((r for r in rows if r['status']=='open'),key=priority,reverse=True)
    claimed_received=sum(r['amount_cents'] for r in rows if r['status'] in ('paid','refunded'))
    restricted=sum(r['amount_cents'] for r in rows if r['restricted'])
    # A human-entered 'verified=True' and reference URI are NOT independent bank
    # transaction confirmation. Deliberately default the provider-verified amount
    # to zero until a real, consented, authenticated reconciliation adapter exists.
    return {'verified_cash_cents':0,'self_reported_cash_cents':claimed_received,
            'proof_status':'bank/provider reconciliation not connected',
            'restricted_potential_cents':restricted,
            'open_count':len(pending),'top_actions':[
            {'title':r['title'],'kind':r['kind'],'amount_cents':r['amount_cents'],
             'verified':bool(r['verified']),'human_gate':r['human_gate'],
             'due_date':r['due_date'],'evidence_url':r['evidence_url']}
            for r in pending[:3]]}

def main():
    p=argparse.ArgumentParser(description='Offline AVA Twin Keeper; no paid service or remote access')
    p.add_argument('--db',default='twin_ledger.sqlite',help='private local SQLite database path')
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('add');a.add_argument('json_file')
    s=sub.add_parser('status');s.add_argument('id');s.add_argument('status');s.add_argument('--receipt',default='')
    sub.add_parser('report')
    args=p.parse_args()
    with connect(args.db) as con:
        try:
            if args.cmd=='add':out=add(con,json.loads(Path(args.json_file).read_text()))
            elif args.cmd=='status':change_status(con,args.id,args.status,args.receipt);out={'updated':True}
            else:out=report(con)
            print(json.dumps(out,indent=2))
        except (GuardError,ValueError) as e:
            p.exit(2,'Rejected: '+str(e)+'\n')
if __name__=='__main__':
    main()