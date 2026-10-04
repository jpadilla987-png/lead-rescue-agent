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

test("search route fails closed on adapter error", async () => {
  const res=responseRecorder();
  const fakeSearch=async()=>{throw new Error("401");};
  await handle(request("POST","/api/search",{anchor:"Agatha Christie"}),res,fakeSearch);
  assert.equal(res.status,400);
  assert.match(JSON.parse(res.body).error,/401/);
});
