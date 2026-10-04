import http from "node:http";
import { integrationStatus, recommendQloo, searchQloo } from "./app.mjs";
import { buildTasteBridge } from "./bridge.mjs";

const port = Number(process.env.PORT || 3000);
const maxBody = 8 * 1024;

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TasteBridge</title>
<style>
body{font-family:system-ui,sans-serif;max-width:820px;margin:42px auto;padding:0 20px;line-height:1.5}
form{display:grid;gap:14px}input[type=text]{padding:12px;font-size:1rem}.domains{display:flex;gap:12px;flex-wrap:wrap}
button{padding:12px 18px;width:max-content}pre{white-space:pre-wrap;background:#f5f5f5;padding:16px;border-radius:8px;overflow:auto}
small{display:block;margin-top:20px}.status{padding:10px 12px;background:#fafafa;border:1px solid #ddd;border-radius:8px}
</style>
</head>
<body>
<h1>TasteBridge</h1>
<p>Start with one public cultural anchor. TasteBridge resolves it in Qloo, then crosses Qloo's taste graph into the domains you choose.</p>
<form id="f">
  <input id="a" type="text" maxlength="120" placeholder="e.g. Agatha Christie, Bauhaus, Brian Eno" required>
  <div class="domains">
    <label><input type="checkbox" name="domain" value="music" checked> Music</label>
    <label><input type="checkbox" name="domain" value="movies" checked> Movies</label>
    <label><input type="checkbox" name="domain" value="books" checked> Books</label>
    <label><input type="checkbox" name="domain" value="places"> Places</label>
    <label><input type="checkbox" name="domain" value="brands"> Brands</label>
    <label><input type="checkbox" name="domain" value="travel"> Travel</label>
  </div>
  <button>Build my cultural bridge</button>
</form>
<p class="status">Qloo is the recommendation engine here: no Qloo signal means no recommendation packet.</p>
<pre id="out">Ready.</pre>
<small>Use public cultural concepts only. Do not enter email, account/device identifiers, private location history, or sensitive personal data.</small>
<script>
const f=document.getElementById("f"),a=document.getElementById("a"),out=document.getElementById("out");
f.addEventListener("submit",async e=>{
  e.preventDefault();
  const domains=[...document.querySelectorAll('input[name="domain"]:checked')].map(x=>x.value);
  out.textContent="Resolving the seed and crossing Qloo's taste graph…";
  try{
    const r=await fetch("/api/bridge",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({anchor:a.value,domains})});
    const j=await r.json();
    if(!r.ok) throw new Error(j.error||"TasteBridge failed");
    out.textContent=JSON.stringify(j,null,2);
  }catch(err){out.textContent="Request failed: "+err.message}
});
</script>
</body>
</html>`;

function send(res, status, body, type="application/json; charset=utf-8") {
  res.writeHead(status, {
    "content-type": type,
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "content-security-policy": "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'",
  });
  res.end(body);
}

async function readJson(req) {
  let size = 0;
  const chunks = [];
  for await (const chunk of req) {
    size += chunk.length;
    if (size > maxBody) throw new Error("request too large");
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

export async function handle(req, res, search = searchQloo, recommend = recommendQloo, bridge = buildTasteBridge) {
  if (req.method === "GET" && req.url === "/") {
    return send(res, 200, html, "text/html; charset=utf-8");
  }
  if (req.method === "GET" && req.url === "/health") {
    return send(res, 200, JSON.stringify({ok:true, service:"tastebridge", qloo:integrationStatus()}));
  }
  if (req.method === "POST" && req.url === "/api/bridge") {
    try {
      const body = await readJson(req);
      const result = await bridge(body.anchor, body.domains);
      return send(res, 200, JSON.stringify(result));
    } catch (error) {
      return send(res, 400, JSON.stringify({error:error.message}));
    }
  }
  if (req.method === "POST" && req.url === "/api/search") {
    try {
      const body = await readJson(req);
      const result = await search(body.anchor);
      return send(res, 200, JSON.stringify(result));
    } catch (error) {
      return send(res, 400, JSON.stringify({error:error.message}));
    }
  }
  if (req.method === "POST" && req.url === "/api/recommend") {
    try {
      const body = await readJson(req);
      const result = await recommend(body.entityId, body.targetType);
      return send(res, 200, JSON.stringify(result));
    } catch (error) {
      return send(res, 400, JSON.stringify({error:error.message}));
    }
  }
  return send(res, 404, JSON.stringify({error:"not found"}));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  http.createServer((req,res)=>handle(req,res)).listen(port, "0.0.0.0", () => {
    console.log(`TasteBridge listening on :${port}`);
  });
}
