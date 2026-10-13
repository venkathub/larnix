const test=require('node:test'),assert=require('node:assert/strict');
const {step,threshold}=require('../samples/foundations/mini-math.js');
const {evidence}=require('../samples/foundations/lesson.js');
const {spawnSync}=require('node:child_process');
const path=require('node:path');

test('case evidence escapes text and preserves only newline values as preformatted',()=>{
 assert.equal(evidence([['Label <&>', '  <script>\n"quoted" & \'text\'']]),
  '<dl class="case-evidence"><div><dt>Label &lt;&amp;&gt;</dt><dd><pre class="evidence-pre">  &lt;script&gt;\n&quot;quoted&quot; &amp; &#x27;text&#x27;</pre></dd></div></dl>');
 assert.equal(evidence([['Input','“  Drill STOPPED  ”']]),
  '<dl class="case-evidence"><div><dt>Input</dt><dd>“  Drill STOPPED  ”</dd></div></dl>');
});

test('client evidence builder equals the Python renderer for every authored case',()=>{
 const script="import json, sys; sys.path.insert(0, 'scripts'); from render_foundations import load_notes, evidence; print(json.dumps([[c['evidence'], evidence(c['evidence'])] for n in load_notes().values() for c in n['lab']['scenarios']]))";
 const result=spawnSync('python3',['-c',script],{cwd:path.resolve(__dirname,'..'),encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);
 const cases=JSON.parse(result.stdout);
 assert.ok(cases.length>0);
 for(const [rows,html] of cases) assert.equal(evidence(rows),html);
});
test('quadratic step agrees with slope and loss; rate changes convergence',()=>{
 assert.deepEqual(step(0,.5),{before:0,gradient:-6,weight:3,loss:0});
 assert.equal(step(step(0,1).weight,1).weight,0);
 let small=0,big=0;for(let i=0;i<4;i++){small=step(small,.25).weight;big=step(big,1.2).weight;}
 assert.ok((small-3)**2<9);assert.ok((big-3)**2>9);
 assert.equal(step(3,.25).weight,3);assert.throws(()=>step(1,NaN),RangeError);
});
test('threshold counts include ties and preserve undefined precision',()=>{
 assert.equal(threshold(.7).reviewed,3);
 assert.equal(threshold(.4).recall,1);
 const none=threshold(1);assert.equal(none.reviewed,0);assert.equal(none.precision,null);assert.equal(none.fn,3);
 assert.equal(threshold(0).fp,3);assert.throws(()=>threshold(-.1),RangeError);
 for(let i=0;i<=10;i++){const s=threshold(i/10);assert.equal(s.tp+s.fn,3);assert.equal(s.tp+s.fp,s.reviewed);}
});
