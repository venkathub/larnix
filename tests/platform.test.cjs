const test=require('node:test'),assert=require('node:assert/strict');
const {search,correctChecks}=require('../web/catalog.js');
const {clean,create}=require('../web/progress.js');
const data=require('../docs/curriculum/curriculum.json'),previews=require('../web/lessons.json');
const base={tracks:data.tracks,previews};
const count=results=>results.reduce((n,m)=>n+m.lessons.length,0);
test('catalogue keeps 188 plans distinct from implemented previews',()=>{
 assert.equal(count(search(data.modules,base)),188);
 assert.equal(count(search(data.modules,{...base,availability:'interactive'})),Object.keys(previews).length);
 assert.equal(count(search(data.modules,{...base,availability:'planned'})),188-Object.keys(previews).length);
});
test('topic search is case-insensitive and combines track and availability filters',()=>{
 const results=search(data.modules,{...base,query:'RAG pipeline',track:'T3',availability:'interactive'});
 assert.deepEqual(results.flatMap(m=>m.lessons.map(l=>l.id)),['M17-L01']);
 assert.equal(count(search(data.modules,{...base,query:'not-a-real-topic'})),0);
 assert.equal(count(search(data.modules,{...base,track:'bad'})),0);
});
test('interview and production views search their respective authored plan fields',()=>{
 assert.ok(count(search(data.modules,{...base,view:'interview',query:'ticket routing'}))>0);
 assert.ok(count(search(data.modules,{...base,view:'production',query:'fictional equipment-rental support desk'}))>0);
 assert.equal(count(search(data.modules,{...base,availability:'bookmarked',bookmarked:['M01-L01']})),1);
});
const storage=()=>{let value=null;return{getItem:()=>value,setItem:(_,next)=>{value=next;}};};
test('progress persists independent flags and answers across instances',()=>{
 const disk=storage(),a=create(disk);a.update('M03-L01',{read:true,answers:{prediction:'b'}});a.update('M03-L01',{bookmarked:true});a.visit('M03-L01');
 const b=create(disk),saved=b.load();assert.equal(saved.lastLesson,'M03-L01');assert.equal(saved.lessons['M03-L01'].exercise,false);assert.equal(saved.lessons['M03-L01'].read,true);assert.equal(saved.lessons['M03-L01'].bookmarked,true);assert.equal(correctChecks(saved.lessons['M03-L01'],previews['M03-L01']),1);
 b.update('M03-L01',{answers:{prediction:'a'}});assert.equal(correctChecks(b.load().lessons['M03-L01'],previews['M03-L01']),0);
 b.reset();assert.deepEqual(b.load().lessons,{});assert.equal(b.load().lastLesson,null);
});
test('unavailable storage retains page memory through theme and visit updates',()=>{
 const store=create({getItem(){throw Error('disabled');},setItem(){throw Error('disabled');}});
 store.update('M03-L01',{read:true});store.setTheme('light');store.visit('M03-L01');
 assert.equal(store.isPersistent(),false);assert.equal(store.load().lessons['M03-L01'].read,true);assert.equal(store.load().theme,'light');
});
test('malformed, future-schema and invalid progress are handled without fabricated mastery',()=>{
 assert.deepEqual(clean({version:2,lessons:{'M01-L01':{read:true}}}).lessons,{});
 const p=clean({version:1,lessons:{bad:{read:true},'M01-L01':{read:'yes',exercise:1,answers:{x:9}}}});
 assert.deepEqual(p.lessons,{'M01-L01':{read:false,exercise:false,bookmarked:false,answers:{}}});
 const store=create({getItem(){return '{invalid';},setItem(){}});assert.deepEqual(store.load().lessons,{});assert.doesNotThrow(()=>store.update('M03-L01',{read:true}));
});
