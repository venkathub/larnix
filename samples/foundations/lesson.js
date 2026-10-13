/* Case explorer for original foundation lessons. Fixed, inspectable teaching
   fixtures; never claims to train a model, run Python or call an external API. */
(function(){
 'use strict';
 const escape=text=>String(text).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#x27;'}[char]));
 function evidence(rows){
  return '<dl class="case-evidence">'+rows.map(([label,value])=>{
   const text=String(value),content=text.includes('\n')?`<pre class="evidence-pre">${escape(text)}</pre>`:escape(text);
   return `<div><dt>${escape(label)}</dt><dd>${content}</dd></div>`;
  }).join('')+'</dl>';
 }
 if(typeof module==='object'&&module.exports){module.exports={evidence};return;}
 const lesson=window.FoundationLesson,$=id=>document.getElementById(id);
 const element=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);if(cls)n.className=cls;return n;};
 function render(index){
  const selected=lesson.lab.scenarios[index];
  document.querySelectorAll('[data-case]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.case)===index)));
  $('case-result').textContent=selected.result;$('case-why').textContent=selected.why;
  // The same diagram nodes preserve reading position as the selected case changes.
  $('case-visual').querySelectorAll('.case-stages strong').forEach((n,i)=>n.textContent=selected.steps[i]);
  const bars=element('div',undefined,'case-bars');bars.setAttribute('aria-label','Compare the quantities');
  selected.bars.forEach(b=>{const row=element('div',undefined,'case-bar'),heading=element('div');heading.append(element('span',b.label),element('strong',b.value));const track=element('span',undefined,'bar-track'),ink=element('span');track.setAttribute('aria-hidden','true');ink.style.width=`${100*b.value/b.max}%`;track.append(ink);row.append(heading,track);bars.append(row);});
  $('case-visual').querySelector('.case-bars').replaceWith(bars);
  $('case-visual').querySelector('.case-evidence').outerHTML=evidence(selected.evidence);
 }
 document.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>render(Number(b.dataset.case))));
 const questions=Object.fromEntries(lesson.checks.map((q,i)=>[`check${i+1}`,{answer:String(q.answer),correct:'Correct. '+q.explanation,wrong:'Reconsider the mechanism. '+q.explanation}]));
 window.LessonUI.init({id:lesson.id,questions});
})();
