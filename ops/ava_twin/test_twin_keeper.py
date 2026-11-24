import tempfile,unittest
from pathlib import Path
from twin_keeper import connect,add,report,change_status,GuardError
class TwinKeeperTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.con=connect(Path(self.tmp.name)/'a.sqlite')
  self.sample={'title':'Example refundable fee','kind':'refund','amount_cents':3000,'lineage':'Bank transaction 234','evidence_url':'local://statement-234','verified':True,'effort_minutes':5}
 def tearDown(self):self.con.close();self.tmp.cleanup()
 def test_record(self):self.assertTrue(add(self.con,self.sample)['new'])
 def test_duplicate_lineage(self):
  add(self.con,self.sample);self.assertFalse(add(self.con,self.sample)['new']);self.assertEqual(report(self.con)['open_count'],1)
 def test_persists(self):
  add(self.con,self.sample);self.assertEqual(self.con.execute('SELECT count(*) FROM leads').fetchone()[0],1)
 def test_no_invented_money(self):
  add(self.con,self.sample);self.assertEqual(report(self.con)['verified_cash_cents'],0)
 def test_no_paid_without_receipt(self):
  x=add(self.con,self.sample)['id']
  with self.assertRaises(GuardError):change_status(self.con,x,'paid')
 def test_paid_requires_verified(self):
  o=dict(self.sample);o['verified']=False;x=add(self.con,o)['id']
  with self.assertRaises(GuardError):change_status(self.con,x,'paid','local://bank-confirmed')
 def test_cash_with_receipt(self):
  x=add(self.con,self.sample)['id'];change_status(self.con,x,'refunded','local://bank-posted-refund')
  self.assertEqual(report(self.con)['verified_cash_cents'],3000)
 def test_restricted_not_spendable(self):
  o=dict(self.sample);o['restricted']=True;x=add(self.con,o)['id']
  with self.assertRaises(GuardError):change_status(self.con,x,'paid','local://restricted-funds')
 def test_missing_source(self):
  o=dict(self.sample);o['lineage']=''
  with self.assertRaises(GuardError):add(self.con,o)
 def test_negative_amount(self):
  o=dict(self.sample);o['amount_cents']=-1
  with self.assertRaises(GuardError):add(self.con,o)
 def test_unsafe_source(self):
  o=dict(self.sample);o['evidence_url']='javascript:alert(1)'
  with self.assertRaises(GuardError):add(self.con,o)
 def test_true_idempotency_across_restart(self):
  r=add(self.con,self.sample);self.con.close();self.con=connect(Path(self.tmp.name)/'a.sqlite')
  self.assertFalse(add(self.con,self.sample)['new']);self.assertEqual(report(self.con)['open_count'],1)
if __name__=='__main__':unittest.main(verbosity=2)