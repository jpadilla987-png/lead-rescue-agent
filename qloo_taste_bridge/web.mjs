import http from "node:http";
import { searchQloo } from "./app.mjs";

const port = Number(process.env.PORT || 3000);
const maxBody = 8 * 1024;

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TasteBridge</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:48px auto;padding:0 20px;line-height:1.5}
form{display:flex;gap:8px;flex-wrap:wrap}input{flex:1;min-width:260px;padding:12px}button{padding:12px 18px}
pre{white-space:pre-wrap;background:#f5f5f5;padding:16px;border-radius:8px}
small{display:block;margin-top:20px}
</style>
</head>
<body>
<h1>TasteBridge</h1>
<p>Resolve a public cultural anchor through Qloo and return a provenance-first evidence packet.</p>
<form id="f"><input id="a" maxlength="120" placeholder="e.g. Agatha Christie" required><button>Search Qloo</button></form>
<pre id="out">Ready.</pre>
<small>No email, account ID, device ID, or private location history should be entered.</small>
<script>
const f=document.getElementById("f"),a=document.getElementById("a"),out=document.getElementById("out");
f.addEventListener("submit",async e=>{
 e.preventDefault(); out.textContent="Working…";
 try{
  const r=await fetch("/api/search",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({anchor:a.value})});
  const j=await r.json(); out.textContent=JSON.stringify(j,null,2);
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

export async function handle(req, res, search = searchQloo) {
  if (req.method === "GET" && req.url === "/") {
    return send(res, 200, html, "text/html; charset=utf-8");
  }
  if (req.method === "GET" && req.url === "/health") {
    return send(res, 200, JSON.stringify({ok:true, service:"tastebridge"}));
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
  return send(res, 404, JSON.stringify({error:"not found"}));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  http.createServer((req,res)=>handle(req,res)).listen(port, "0.0.0.0", () => {
    console.log(`TasteBridge listening on :${port}`);
  });
}
