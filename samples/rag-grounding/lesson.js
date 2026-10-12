(function(){
 'use strict';
 const R=window.RagLesson, $=id=>document.getElementById(id);
 let state=R.defaults();
 const el=(tag,text,className)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(className)n.className=className;return n;};
 const scenarios={
  baseline:()=>R.defaults(),tight:()=>({...R.defaults(),slots:1}),miss:()=>({...R.defaults(),topK:2}),
  stale:()=>({...R.defaults(),available:['R1','F1','H1'],currentOnly:false}),
  conflict:()=>({...R.defaults(),available:['R2','R3','F1','H1'],topK:4,slots:3}),
  unknown:()=>({...R.defaults(),question:'damage',topK:5,slots:5})
 };
 R.docs.forEach(d=>{
  const card=el('article',undefined,'document-card');card.id='source-'+d.id;
  const label=el('label');const check=el('input');check.type='checkbox';check.value=d.id;check.id='include-'+d.id;
  label.append(check,el('span',d.id+' · '+d.title));
  card.append(label,el('p',d.text),el('p',`Effective ${d.from} → ${d.to||'no end date'} · ${R.current(d)?'valid on reference date':'expired'}`,'help'));
  check.addEventListener('change',()=>{state.available=R.docs.filter(doc=>$('include-'+doc.id).checked).map(doc=>doc.id);render(true);});
  $('documents').append(card);
 });
 function render(announce=false){
  const result=R.run(state);
  $('question').value=state.question;$('top-k').value=state.topK;$('slots').value=state.slots;$('current-only').checked=state.currentOnly;
  R.docs.forEach(d=>{$('include-'+d.id).checked=state.available.includes(d.id);$('source-'+d.id).classList.toggle('unavailable',!state.available.includes(d.id));});
  $('question-text').textContent=result.question;
  const stages=[['Retrieve',result.candidates.length+' candidates'],['Select',result.decisions.filter(d=>!d.reason.startsWith('Excluded')).length+' eligible'],['Context',result.context.length+' passages'],['Mock generate','Check required facts'],['Cite / abstain',result.status==='answer'?'Cited answer':result.status==='conflict'?'Conflict':'Evidence gap']];
  $('pipeline').replaceChildren(...stages.map(([title,value],i)=>{const li=el('li');li.append(el('span',String(i+1).padStart(2,'0'),'stage-number'),el('strong',title),el('span',value));return li;}));
  $('trace').replaceChildren(...result.candidates.map((d,i)=>{const li=el('li');li.append(el('strong',`${i+1}. ${d.id} · ${d.title}`),el('p',result.decisions[i].reason));return li;}));
  if(!result.candidates.length)$('trace').append(el('li','No available passages.'));
  $('context').replaceChildren(...result.context.map(d=>{const passage=el('div',undefined,'context-passage');passage.id='context-'+d.id;passage.tabIndex=-1;passage.append(el('strong','['+d.id+'] '+d.title),el('p',d.text));return passage;}));
  if(!result.context.length)$('context').append(el('p','No passages supplied.'));
  const found=result.candidates.map(d=>d.id),packed=result.context.map(d=>d.id);
  $('nearby-trace').textContent=`Found: ${found.join(' + ')||'none'} → Sent to model: ${packed.join(' + ')||'none'}`;
  let nearbyResult,nearbyWhy;
  if(result.stale.length&&result.status==='answer'){nearbyResult='A cited answer includes expired evidence.';nearbyWhy='The source is traceable but out of date. Check policy validity before trusting the answer.';}
  else if(result.status==='conflict'){nearbyResult='Conflicting policies: the lab withholds a definitive answer.';nearbyWhy='Visible sources disagree. Resolve authority or precedence; retrieval order is not a policy rule.';}
  else if(result.status==='answer'){nearbyResult=result.claims.map(c=>c.text).join(' ');nearbyWhy='The needed facts reached context. The lab can cite each claim; a real generator still needs evaluation.';}
  else if(state.question==='return'&&found.includes('F1')&&!packed.includes('F1')){nearbyResult='The fee disappeared. This lab withholds a complete answer.';nearbyWhy='F1 was retrieved but dropped from context. Inspect selection and packing, not retrieval alone.';}
  else if(state.question==='return'&&!found.includes('F1')){nearbyResult='The fee never reached the answer.';nearbyWhy='F1 was not retrieved. Inspect source availability, query and ranking; a larger context alone cannot help.';}
  else {nearbyResult='Required evidence is missing: the lab withholds a complete answer.';nearbyWhy='Compare the source folder, retrieved candidates and supplied context to find where the required fact is missing.';}
  $('nearby-result').textContent=nearbyResult;$('nearby-why').textContent=nearbyWhy;
  $('answer').textContent=result.answer;
  $('quick-outcome').textContent=result.answer+(result.stale.length?' Warning: expired evidence is in context.':'');
  $('answer-status').textContent=result.status==='answer'?'Cited answer':result.status==='conflict'?'Conflict — abstain':'Missing evidence — abstain';
  $('answer-status').dataset.status=result.status;
  $('validity-warning').hidden=!result.stale.length;
  $('validity-warning').textContent=`Date audit: context includes expired evidence (${result.stale.join(', ')}). A citation is not proof this answer applies on ${R.asOf}.`;
  $('support').replaceChildren();
  if(result.claims.length){
   $('support').append(el('p',result.status==='answer'?'Claim-to-source map · select a citation to inspect its passage':'Supported fragments · withheld from the complete answer','eyebrow'));
   result.claims.forEach(c=>{const row=el('div',undefined,'support-row');row.append(el('span',c.text));c.citations.forEach(id=>{const link=el('a','['+id+']');link.href='#context-'+id;link.setAttribute('aria-label','Inspect citation '+id);row.append(link);});$('support').append(row);});
  }else $('support').append(el('p','No unambiguous supported claims to display.','help'));
  document.querySelectorAll('[data-scenario]').forEach(b=>{const config=scenarios[b.dataset.scenario]();const match=['question','topK','slots','currentOnly'].every(k=>config[k]===state[k])&&config.available.join(',')===state.available.join(',');b.setAttribute('aria-pressed',String(match));});

 }
 ['question','top-k','slots','current-only'].forEach(id=>$(id).addEventListener('change',()=>{
  state.question=$('question').value;state.topK=Number($('top-k').value);state.slots=Number($('slots').value);state.currentOnly=$('current-only').checked;render(true);
 }));
 document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>{state=scenarios[b.dataset.scenario]();render(true);}));
 $('reset-lab').addEventListener('click',()=>{state=R.defaults();render(true);});
 const quizzes={
  source:{answer:'source',yes:'Yes. The citation traces the claim to a source. You must separately check whether that source applies to the customer’s date and rental.',no:'A real citation can point to expired evidence. Check provenance and applicability separately.'},
  context:{answer:'context',yes:'Exactly. F1 was found but dropped before generation. Inspect the context budget and selection strategy first.',no:'The trace already shows the document was retrieved. Find the boundary after retrieval where F1 was removed.'},
  unknown:{answer:'abstain',yes:'Correct. Seek the missing authoritative policy or route the question to the help desk. Neither a larger K nor a plausible guess creates evidence.',no:'The deposit is absent from the entire source collection. A fee is a different fact, and retrieving every passage cannot supply the missing deposit.'}
 };
 const questions=Object.fromEntries(Object.entries(quizzes).map(([key,q])=>[key,{answer:q.answer,correct:q.yes,wrong:q.no}]));
 window.LessonUI.init({id:'M17-L01',questions});
 render();
})();
