const test = require('node:test');
const assert = require('node:assert/strict');
const M = require('../vector-math.js');
const near = (a,b) => assert.ok(Math.abs(a-b) < 1e-12, `${a} != ${b}`);
test('the original fixture reverses ranking between dot and cosine', () => {
  const q=[1,0], a=[1,0], b=[2,2];
  assert.equal(M.dot(q,a),1);assert.equal(M.dot(q,b),2);
  near(M.cosine(q,a),1);near(M.cosine(q,b),1/Math.sqrt(2));
});
test('normalization removes positive magnitude and matches cosine', () => {
  for(const d of [[1,0],[2,2],[-1,0],[0,1]]) {
    near(M.cosine([1,0],d),M.score([1,0],d,'dot',true));
    near(M.cosine([1,0],d),M.cosine([3,0],d.map(x=>x*2)));
  }
});
test('undefined zero directions are distinct from valid zero and negative scores', () => {
  assert.equal(M.dot([1,0],[0,0]),0);
  assert.equal(M.cosine([1,0],[0,0]),null);
  assert.equal(M.cosine([0,0],[1,0]),null);
  assert.equal(M.score([0,0],[1,0],'dot',true),null);
  assert.equal(M.cosine([1,0],[0,1]),0);
  assert.equal(M.cosine([1,0],[-2,0]),-1);
});
test('projection reconstructs the aligned component and rejects a zero axis', () => {
  const p=M.projection([2,2],[1,0]);assert.deepEqual(p,[2,0]);
  assert.equal(M.projection([2,2],[0,0]),null);
  const v=[1,3],q=[2,-1],proj=M.projection(v,q);
  near(M.dot(v.map((x,i)=>x-proj[i]),q),0);
});
test('dimension mismatches and invalid vectors are rejected', () => {
  assert.throws(()=>M.dot([1,2],[1]),RangeError);
  assert.throws(()=>M.dot([1,NaN],[1,0]),TypeError);
  assert.throws(()=>M.cosine([Infinity,0],[1,0]),TypeError);
  assert.throws(()=>M.normalize([]),TypeError);
  assert.throws(()=>M.score([1,0],[1,0],'invented'),RangeError);
});
