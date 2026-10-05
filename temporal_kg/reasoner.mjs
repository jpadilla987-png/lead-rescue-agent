export function reasonAt({queryTime, claims, evidence}) {
  const tq = Date.parse(queryTime);
  if (!Number.isFinite(tq)) throw new Error("invalid queryTime");
  const ev = new Map(evidence.map(e => [e.id, e]));
  const packet = { queryTime, assertions: [], unresolved: [], violations: [] };
  for (const c of claims) {
    const start = c.validFrom ? Date.parse(c.validFrom) : -Infinity;
    const end = c.validUntil ? Date.parse(c.validUntil) : Infinity;
    if (!(start <= tq && tq <= end)) continue;
    const eligible = [], future = [];
    for (const id of c.evidenceIds || []) {
      const e = ev.get(id);
      if (!e) continue;
      const at = Date.parse(e.availableAt);
      if (at <= tq) eligible.push(id); else future.push(id);
    }
    if (future.length) packet.violations.push({claim:c.id,type:"FUTURE_EVIDENCE_EXCLUDED",evidenceIds:future});
    if (!eligible.length) {
      packet.unresolved.push({claim:c.id,state:"UNRESOLVED"});
      continue;
    }
    packet.assertions.push({claim:c.id,state:c.state || "SUPPORTED",evidenceIds:eligible});
  }
  return packet;
}
