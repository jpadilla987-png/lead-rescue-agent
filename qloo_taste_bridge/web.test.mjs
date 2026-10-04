import test from "node:test";
import assert from "node:assert/strict";
import { handle } from "./web.mjs";

function responseRecorder() {
  return {
    status: null, headers: null, body: "",
    writeHead(status, headers){ this.status=status; this.headers=headers; },
    end(body=""){ this.body += body; },
  };
}

function request(method, url, payload = null) {
  return {
    method,
    url,
    async *[Symbol.asyncIterator]() {
      if (payload !== null) yield Buffer.from(JSON.stringify(payload));
    },
  };
}

test("health endpoint responds without exposing credentials", async () => {
  const res=responseRecorder();
  await handle(request("GET","/health"),res);
  assert.equal(res.status,200);
  const body=JSON.parse(res.body);
  assert.equal(body.service,"tastebridge");
  assert.equal(typeof body.qloo.connected,"boolean");
  assert.equal(JSON.stringify(body).includes("QLOO_API_KEY"),false);
});

test("bridge route returns Qloo-dependent cross-domain packet", async () => {
  const res=responseRecorder();
  const fakeSearch=async()=>({candidates:[]});
  const fakeRecommend=async()=>({recommendations:[]});
  const fakeBridge=async(anchor,domains)=>({
    source:"qloo",
    mode:"cross-domain-taste-bridge",
    query:anchor,
    domains,
    seed:{id:"urn:seed:1",name:"Agatha Christie"},
    recommendations:{books:[{name:"Book Pick",affinity:0.9}]},
    provenance:{qlooRequired:true},
  });
  await handle(request("POST","/api/bridge",{anchor:"Agatha Christie",domains:["books"]}),res,fakeSearch,fakeRecommend,fakeBridge);
  assert.equal(res.status,200);
  const body=JSON.parse(res.body);
  assert.equal(body.mode,"cross-domain-taste-bridge");
  assert.equal(body.provenance.qlooRequired,true);
});

test("search route uses server-side Qloo adapter", async () => {
  const res=responseRecorder();
  const fakeSearch=async anchor=>({source:"Qloo search",query:anchor,candidates:[{id:"x1",name:"Agatha Christie"}]});
  await handle(request("POST","/api/search",{anchor:"Agatha Christie"}),res,fakeSearch);
  assert.equal(res.status,200);
  assert.equal(JSON.parse(res.body).candidates[0].id,"x1");
});

test("recommend route uses Qloo insights adapter", async () => {
  const res=responseRecorder();
  const fakeSearch=async()=>({candidates:[]});
  const fakeRecommend=async (entityId,targetType)=>({source:"Qloo insights",anchor_entity_id:entityId,target_type:targetType,recommendations:[{id:"m1",name:"Knives Out"}]});
  await handle(request("POST","/api/recommend",{entityId:"urn:entity:book:abc",targetType:"movie"}),res,fakeSearch,fakeRecommend);
  assert.equal(res.status,200);
  const body=JSON.parse(res.body);
  assert.equal(body.target_type,"movie");
  assert.equal(body.recommendations[0].name,"Knives Out");
});

test("bridge route fails closed on adapter error", async () => {
  const res=responseRecorder();
  const fakeSearch=async()=>({candidates:[]});
  const fakeRecommend=async()=>({recommendations:[]});
  const fakeBridge=async()=>{throw new Error("Qloo unavailable");};
  await handle(request("POST","/api/bridge",{anchor:"Agatha Christie",domains:["books"]}),res,fakeSearch,fakeRecommend,fakeBridge);
  assert.equal(res.status,400);
  assert.match(JSON.parse(res.body).error,/Qloo unavailable/);
});
