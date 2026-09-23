from __future__ import annotations

from fastapi.responses import HTMLResponse

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NIGHTEYE Evidence Engine</title>
<style>
:root{font-family:Inter,system-ui,sans-serif;background:#07111f;color:#eef6ff}*{box-sizing:border-box}
body{margin:0;background:radial-gradient(circle at 12% 0,#16324f 0,#07111f 42%,#02060c 100%);min-height:100vh}
main{max-width:1100px;margin:auto;padding:34px 20px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:#7dd3fc;font-size:12px}
h1{font-size:clamp(40px,7vw,70px);line-height:.95;margin:8px 0 16px}.sub{color:#b8c8d9;max-width:800px;font-size:18px;line-height:1.55}
.grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:18px;margin-top:26px}.panel{background:rgba(9,22,38,.9);border:1px solid #19344f;border-radius:20px;padding:20px}
label{display:block;color:#9cc3dd;font-size:13px;margin:12px 0 6px}input,textarea{width:100%;border:1px solid #244864;background:#05101d;color:#eef6ff;border-radius:12px;padding:11px;font:inherit}
textarea{min-height:250px;resize:vertical}button{margin-top:14px;border:0;border-radius:12px;background:#0ea5e9;color:#00131e;padding:12px 16px;font-weight:800;cursor:pointer}
pre{white-space:pre-wrap;overflow:auto;background:#030914;border-radius:14px;padding:16px;min-height:430px;color:#bae6fd}.note{font-size:12px;color:#7796aa;margin-top:10px}
.badge{display:inline-block;padding:7px 10px;border:1px solid #24506c;border-radius:999px;color:#a5f3fc;margin-right:7px;font-size:12px}
@media(max-width:800px){.grid{display:block}.panel{margin-bottom:16px}}
</style>
</head>
<body><main>
<p class="eyebrow">Nebius × NVIDIA Global AI Hackathon</p>
<h1>NIGHTEYE<br>Evidence Engine</h1>
<p class="sub">Detect material change without hiding the reasoning. NIGHTEYE separates observation from inference, generates competing explanations, names a falsifier, preserves unknowns, and recommends reversible next actions.</p>
<div><span class="badge">Nebius Token Factory</span><span class="badge">NVIDIA Nemotron</span><span class="badge">Evidence-first</span></div>
<section class="grid">
<div class="panel">
<p class="eyebrow">Evidence packet</p>
<label>Topic</label><input id="topic" value="Has the monitored supplier situation materially changed?">
<label>Evidence (one line each: id | source | time | text)</label>
<textarea id="evidence">ev-001 | supplier-status | 2026-09-22T08:00:00Z | Supplier status page reports normal operations.
ev-002 | shipping-update | 2026-09-22T14:10:00Z | Two scheduled shipments moved from Tuesday to Friday.
ev-003 | account-manager-note | 2026-09-22T15:05:00Z | Account manager says a temporary component shortage is affecting new outbound orders.</textarea>
<button id="run">Analyze with NIGHTEYE</button>
<p class="note">Live analysis requires the server-side Nebius API key. The key is never exposed to this page.</p>
</div>
<div class="panel"><p class="eyebrow">Auditable brief</p><pre id="out">Ready.</pre></div>
</section>
<script>
const out=document.getElementById('out');
document.getElementById('run').onclick=async()=>{
  out.textContent='Analyzing evidence...';
  try{
    const evidence=document.getElementById('evidence').value.trim().split('\n').filter(Boolean).map(line=>{
      const p=line.split('|').map(x=>x.trim()); return {id:p[0],source:p[1],observed_at:p[2],text:p.slice(3).join(' | ')};
    });
    const r=await fetch('/analyze',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({topic:document.getElementById('topic').value,evidence})});
    const data=await r.json(); out.textContent=JSON.stringify(data,null,2);
  }catch(e){out.textContent='Error: '+e.message}
};
</script>
</main></body></html>"""


def home() -> HTMLResponse:
    return HTMLResponse(PAGE)
