const test=require('node:test');
const assert=require('node:assert/strict');
const R=require('../rag-engine.js');
const run=overrides=>R.run({...R.defaults(),...overrides});
test('baseline cites the current return window and fee, excluding expired policy',()=>{
 const r=run({}); assert.equal(r.status,'answer');assert.deepEqual(r.context.map(d=>d.id),['R2','F1']);
 assert.match(r.answer,/3 calendar days/);assert.match(r.answer,/₹200/);
 assert.deepEqual(r.claims.map(c=>c.citations),[['R2'],['F1']]);assert.deepEqual(r.stale,[]);
});
test('a retrieval miss and a context omission have distinct trace evidence',()=>{
 const miss=run({topK:2});const omitted=run({slots:1});
 for(const r of [miss,omitted]){assert.equal(r.status,'abstain');assert.deepEqual(r.missing,['fee']);assert.doesNotMatch(r.answer,/₹200/);}
 assert.ok(!miss.candidates.some(d=>d.id==='F1'));assert.ok(omitted.candidates.some(d=>d.id==='F1'));
 assert.match(omitted.decisions.find(d=>d.id==='F1').reason,/slots full/);
});
test('citation support alone can accompany an expired wrong-for-today answer',()=>{
 const r=run({available:['R1','F1','H1'],currentOnly:false});
 assert.equal(r.status,'answer');assert.match(r.answer,/7 calendar days/);assert.deepEqual(r.stale,['R1']);
 const safe=run({available:['R1','F1','H1']});assert.equal(safe.status,'abstain');assert.deepEqual(safe.missing,['days']);
});
test('contradictory current sources stop the answer, but unseen conflicts are not detected',()=>{
 const r=run({available:['R2','R3','F1','H1'],topK:4,slots:3});
 assert.equal(r.status,'conflict');assert.deepEqual(r.conflicts,['days']);assert.deepEqual(r.claims,[]);
 assert.equal(run({available:['R2','R3','F1','H1'],topK:2}).status,'answer');
});
test('unsupported questions and empty corpora abstain',()=>{
 for(const r of [run({question:'damage',topK:5,slots:5}),run({available:[]})])assert.equal(r.status,'abstain');
 assert.deepEqual(run({question:'damage'}).claims,[]);
});
test('every returned citation points to included evidence with the matching field',()=>{
 for(const question of Object.keys(R.questions))for(let topK=1;topK<=5;topK++)for(let slots=1;slots<=5;slots++)for(const currentOnly of [true,false]){
  const r=run({question,topK,slots,currentOnly,available:R.docs.map(d=>d.id)});
  for(const c of r.claims)for(const id of c.citations)assert.ok(r.context.some(d=>d.id===id&&d.field===c.field));
 }
});
test('invalid controls and unknown or duplicated IDs are rejected',()=>{
 for(const config of [{topK:0},{slots:6},{topK:1.5},{question:'x'},{available:['x']},{available:['R1','R1']},{currentOnly:'yes'}])assert.throws(()=>run(config));
});
test('downloadable cases and policies match the browser fixture',()=>{
 const fixtures=require('../fixtures.json');assert.deepEqual(fixtures.documents,R.docs);assert.deepEqual(fixtures.questions,R.questions);assert.equal(fixtures.asOf,R.asOf);
 for(const c of fixtures.cases){const r=R.run(c.config);assert.deepEqual({status:r.status,context:r.context.map(d=>d.id),claimCitations:r.claims.map(c=>c.citations),missing:r.missing,conflicts:r.conflicts,stale:r.stale},c.expected,c.name);}
});
