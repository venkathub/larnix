const test=require('node:test'),assert=require('node:assert/strict');
const {run,recover}=require('../recovery-engine.js');
const fixtures=require('../fixtures.json');
const summary=s=>({status:s.status,effectCount:s.ledger.length,total:s.ledger.reduce((n,r)=>n+r.amount,0),calls:s.calls,checkpointStatus:s.checkpoint.status,receiptId:s.checkpoint.receipt?.id||null});
test('all independent production fixtures agree with the browser model',()=>{
 for(const c of fixtures.cases)assert.deepEqual(summary(run(c.config).result),c.expected,c.name);
});
test('crash preserves external effect and intent while destroying an unsaved receipt',()=>{
 const {frames}=run({crash:'receipt'}),before=frames.at(-3),crash=frames.at(-2);
 assert.equal(before.memoryReceipt.id,'receipt-1');assert.equal(crash.memoryReceipt,null);
 assert.equal(crash.checkpoint.receipt,null);assert.deepEqual(crash.ledger,before.ledger);
 assert.equal(crash.checkpoint.key,before.checkpoint.key);assert.equal(crash.ledger.length,1);
});
test('blind retry only duplicates when an earlier effect exists and completion was not saved',()=>{
 for(const crash of ['before','commit','receipt','saved']){
  assert.equal(run({crash,policy:'blind'}).result.ledger.length,['commit','receipt'].includes(crash)?2:1);
 }
});
test('safe recovery preserves one bound business effect across every crash boundary',()=>{
 for(const crash of ['before','commit','receipt','saved']){
  const result=run({crash}).result;
  assert.equal(result.ledger.length,1);assert.equal(result.calls,1);
  assert.deepEqual(result.checkpoint.receipt,result.ledger[0]);
  for(const k of ['key','amount','currency','rental'])assert.equal(result.checkpoint.receipt[k],result.checkpoint[k]);
 }
});
test('a second crash before saving the recovered receipt reconciles without another effect',()=>{
 const s=run().result;s.checkpoint.status='pending';s.checkpoint.receipt=null;
 const again=recover(s);assert.equal(again.ledger.length,1);assert.equal(again.calls,1);
 assert.equal(recover(again).calls,1);assert.equal(s.checkpoint.status,'pending','recovery does not mutate input');
});
test('unknown lookup is held until evidence becomes available',()=>{
 for(const crash of ['before','commit']){
  const held=run({crash,lookupOnline:false}).result;
  assert.equal(held.status,'held');assert.equal(held.checkpoint.status,'pending');
  const resumed=recover(held);assert.equal(resumed.status,'complete');assert.equal(resumed.ledger.length,1);
 }
});
test('changed parameters and mismatched receipts cannot silently complete an intent',()=>{
 const s=run({payloadChanged:true}).result;assert.equal(s.status,'blocked');assert.equal(s.calls,1);
 const bad=run().frames.at(-2);bad.ledger[0].currency='USD';
 const result=recover(bad);assert.equal(result.status,'blocked');assert.equal(result.checkpoint.receipt,null);
});
test('invalid configurations fail explicitly and snapshots are independent',()=>{
 for(const c of [{crash:'maybe'},{policy:'anything'},{lookupOnline:'yes'},{payloadChanged:1}])assert.throws(()=>run(c),TypeError);
 const a=run(),b=run();a.frames[0].checkpoint.amount=1;
 assert.equal(a.result.checkpoint.amount,500);assert.deepEqual(a.result,b.result);
});
test('all 32 control combinations distinguish successful, duplicate, wrong and unresolved outcomes',()=>{
 for(const crash of ['before','commit','receipt','saved'])for(const policy of ['safe','blind'])for(const lookupOnline of [true,false])for(const payloadChanged of [true,false]){
  const s=run({crash,policy,lookupOnline,payloadChanged}).result;
  if(s.status==='complete'){
   assert.equal(s.ledger.length,1);assert.equal(s.ledger[0].amount,500);
   assert.deepEqual(s.checkpoint.receipt,s.ledger[0]);
  }else if(s.status==='duplicate')assert.equal(s.ledger.length,2);
  else if(s.status==='incorrect'){assert.equal(s.ledger.length,1);assert.equal(s.ledger[0].amount,700);}
  else{assert.equal(s.checkpoint.status,'pending');assert.equal(s.checkpoint.receipt,null);}
 }
});
