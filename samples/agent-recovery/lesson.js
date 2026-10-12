(function(){
 'use strict';
 const $=id=>document.getElementById(id),E=window.RecoveryEngine;
 let run,cursor;
 const scenarios={blind:{crash:'commit',policy:'blind'},safe:{crash:'commit',policy:'safe'},before:{crash:'before'},receipt:{crash:'receipt'},saved:{crash:'saved'},unknown:{lookupOnline:false},changed:{payloadChanged:true}};
 function element(tag,text,className){const el=document.createElement(tag);el.textContent=text;if(className)el.className=className;return el;}
 function render(){
  const s=run.frames[cursor],end=cursor===run.frames.length-1;
  $('step-count').textContent=`Step ${cursor+1} / ${run.frames.length}`;
  $('step-back').disabled=cursor===0;$('step-next').disabled=end;
  $('timeline').replaceChildren(...run.frames.map((f,i)=>{const li=element('li',f.status==='crashed'?'Crash':i===0?'Save intent':i===run.frames.length-1?'Recover':i===1?'Dispatch':i===2?'Commit':i===3?'Receive':'Save receipt',i===cursor?'current':i<cursor?'past':'');if(i===cursor)li.setAttribute('aria-current','step');return li;}));
  $('checkpoint-status').textContent=s.checkpoint.status==='done'?'Done · receipt saved':'Pending · receipt absent';
  $('checkpoint-key').textContent=s.checkpoint.key;
  $('checkpoint-receipt').textContent=s.checkpoint.receipt?s.checkpoint.receipt.id:'No saved receipt';
  $('memory-status').textContent=s.memoryReceipt?s.memoryReceipt.id:'No receipt in memory';
  $('effect-count').textContent=String(s.ledger.length)+' effect'+(s.ledger.length===1?'':'s');
  $('total').textContent='₹'+s.ledger.reduce((sum,r)=>sum+r.amount,0)+' recorded · '+s.calls+' tool call'+(s.calls===1?'':'s');
  $('ledger').replaceChildren(...s.ledger.map(r=>element('p',`${r.id} · ₹${r.amount} · ${r.key}`,'ledger-row')));
  $('event').textContent=s.event;
  $('outcome').dataset.status=s.status;
  const labels={running:'IN PROGRESS',crashed:'STOPPED · READY TO RECOVER',complete:'COMPLETE · ONE BUSINESS EFFECT',duplicate:'DUPLICATE · TWO BUSINESS EFFECTS',incorrect:'INCORRECT · WRONG AMOUNT',held:'HELD · COMPLETION UNKNOWN',blocked:'BLOCKED · CHANGED PARAMETERS'};
  $('outcome-label').textContent=labels[s.status];
  $('invariant').textContent=end?(s.status==='complete'?'One ₹500 effect is recorded, and the checkpoint contains its receipt.':s.status==='duplicate'?'The agent saved a completion record, but the provider recorded two effects. Local success hid the duplicate.':s.status==='incorrect'?'Only one effect occurred, but it is ₹700 against an authorized ₹500 intent. Counting effects alone misses the incorrect parameters.':'The agent has not claimed completion. Inspect the provider ledger as the lab observer; the agent cannot use this view as evidence.'):'The three panels show different places where information can live. Watch which ones survive the crash.';
 }
 function configure(atStart=false){
  run=E.run({crash:$('crash-point').value,policy:$('recovery-policy').value,lookupOnline:$('lookup-online').checked,payloadChanged:$('payload-changed').checked});
  cursor=atStart?0:run.frames.length-2;render();
 }
 document.querySelectorAll('[data-scenario]').forEach(button=>button.addEventListener('click',()=>{
  const c={...E.defaults,...scenarios[button.dataset.scenario]};$('crash-point').value=c.crash;$('recovery-policy').value=c.policy;$('lookup-online').checked=c.lookupOnline;$('payload-changed').checked=c.payloadChanged;configure();
 }));
 ['crash-point','recovery-policy','lookup-online','payload-changed'].forEach(id=>$(id).addEventListener('change',()=>configure()));
 $('step-back').addEventListener('click',()=>{cursor=Math.max(0,cursor-1);render();});
 $('step-next').addEventListener('click',()=>{cursor=Math.min(run.frames.length-1,cursor+1);render();});
 $('run-end').addEventListener('click',()=>{cursor=run.frames.length-1;render();});
 $('restart-trace').addEventListener('click',()=>{cursor=0;render();});
 window.LessonUI.init({id:'M21-L02',questions:{
  prediction:{answer:'unknown',correct:'Yes. The provider may have committed even though the agent did not save a receipt. Missing local evidence does not establish remote failure.',wrong:'A checkpoint tells you what was saved locally. It does not undo or reliably describe an external action in the crash window.'},
  identity:{answer:'same',correct:'Yes. Keep the operation ID and exact parameters bound to the original intent. A new key can look like a new business action to the provider.',wrong:'A retry attempts the same authorized business action. Changing its identity or amount breaks that relationship.'},
  outage:{answer:'hold',correct:'Yes. Under this lab’s recovery policy, hold and retry reconciliation later. A failed lookup is not an authoritative “not found”.',wrong:'An unavailable lookup provides no evidence that the effect is absent. Keep the original identity and do not invent a new action.'}
 }});
 configure();
})();
