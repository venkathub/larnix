/* Common explanatory checks and theme controls for authored Larnix lessons. */
(function(){
 'use strict';
 window.LessonUI={init({id,questions}){
  const $=id=>document.getElementById(id),checked=new Set();
  const store=document.documentElement.dataset.platformLesson?window.LarnixProgress:null;
  // Optional sections still open when reached through a course or citation link.
  function revealAnchor(){
   let anchor;try{anchor=decodeURIComponent(location.hash.slice(1));}catch{return;}
   const target=document.getElementById(anchor);if(!target)return;
   let node=target,opened=false;
   while(node){if(node.tagName==='DETAILS'&&!node.open){node.open=true;opened=true;}node=node.parentElement;}
   if(opened)target.scrollIntoView({block:'start'});
  }
  window.addEventListener('hashchange',revealAnchor);
  document.addEventListener('click',event=>{
   const link=event.target.closest('a[href^="#"]');
   if(link&&link.hash===location.hash)revealAnchor();
  });
  revealAnchor();
  function progress(){
   $('check-progress').textContent=`${checked.size} / ${Object.keys(questions).length} checks correct`;
   $('completion-title').textContent=`${checked.size} of ${Object.keys(questions).length} answered correctly`;
   if($('completion-text'))$('completion-text').textContent=checked.size===Object.keys(questions).length?'You completed the concept checks. Production practice still needs your implementation and evidence.':'Correct answers unlock a short recap. Production practice is a separate step.';
   if($('recap'))$('recap').hidden=checked.size!==Object.keys(questions).length;
  }
  document.querySelectorAll('[data-quiz]').forEach(quiz=>{
   const key=quiz.dataset.quiz,question=questions[key];
   quiz.querySelectorAll('button').forEach(button=>button.addEventListener('click',()=>{
    const correct=button.dataset.answer===question.answer;
    quiz.querySelectorAll('button').forEach(b=>{b.classList.remove('selected','correct');b.setAttribute('aria-pressed','false');});
    button.classList.add(correct?'correct':'selected');button.setAttribute('aria-pressed','true');
    const feedback=quiz.querySelector('.feedback');feedback.textContent=correct?question.correct:question.wrong;feedback.classList.toggle('success',correct);
    if(correct)checked.add(key);else checked.delete(key);
    if(store){const entry=store.load().lessons[id]||{};store.update(id,{answers:{...entry.answers,[key]:button.dataset.answer}});}
    progress();
   }));
  });
  $('reset-checks').addEventListener('click',()=>{
   checked.clear();document.querySelectorAll('[data-quiz]').forEach(quiz=>{quiz.querySelectorAll('button').forEach(b=>{b.classList.remove('selected','correct');b.setAttribute('aria-pressed','false');});const feedback=quiz.querySelector('.feedback');feedback.textContent='Choose an answer and explain your reasoning.';feedback.classList.remove('success');});
   if(store)store.update(id,{answers:{}});progress();
  });
  function theme(value){document.documentElement.dataset.theme=value;const light=value==='light';$('theme-toggle').textContent=light?'Dark mode ◑':'Light mode ◐';$('theme-toggle').setAttribute('aria-label',`Switch to ${light?'dark':'light'} theme`);}
  theme(store?store.load().theme:document.documentElement.dataset.theme);
  $('theme-toggle').addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='light'?'dark':'light';theme(value);if(store)store.setTheme(value);});
  if(store){const answers=store.load().lessons[id]?.answers||{};document.querySelectorAll('[data-quiz]').forEach(quiz=>{const saved=answers[quiz.dataset.quiz];const button=[...quiz.querySelectorAll('button')].find(b=>b.dataset.answer===saved);if(button)button.click();});}
  progress();
 }};
})();
