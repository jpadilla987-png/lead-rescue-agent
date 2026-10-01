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

function postRequest(payload) {
  return {
    method: "POST",
    url: "/api/search",
    async *[Symbol.asyncIterator]() {
      yield Buffer.from(JSON.stringify(payload));
    },
  };
}

test("health endpoint responds", async () => {
  const res=responseRecorder();
  await handle({method:"GET",url:"/health"},res);
  assert.equal(res.status,200);
  assert.deepEqual(JSON.parse(res.body),{ok:true,service:"tastebridge"});
});

test("search route uses server-side Qloo adapter", async () => {
  const res=responseRecorder();
  const fakeSearch=async anchor=>({source:"qloo",query:anchor,result:{results:[{id:"x1"}]}});
  await handle(postRequest({anchor:"Agatha Christie"}),res,fakeSearch);
  assert.equal(res.status,200);
  assert.equal(JSON.parse(res.body).query,"Agatha Christie");
});

test("search route fails closed on adapter error", async () => {
  const res=responseRecorder();
  const fakeSearch=async()=>{throw new Error("401");};
  await handle(postRequest({anchor:"Agatha Christie"}),res,fakeSearch);
  assert.equal(res.status,400);
  assert.match(JSON.parse(res.body).error,/401/);
});
