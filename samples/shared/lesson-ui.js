/* Common explanatory checks and theme controls for authored Larnix lessons. */
(function(){
 'use strict';
 window.LessonUI={init({id,questions}){
  const $=id=>document.getElementById(id),checked=new Set();
  const store=document.documentElement.dataset.platformLesson?window.LarnixProgress:null;
  function progress(){
   $('check-progress').textContent=`${checked.size} / ${Object.keys(questions).length} checks understood`;
   $('completion-title').textContent=`${checked.size} of ${Object.keys(questions).length} understood`;
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
  if(store)theme(store.load().theme);
  $('theme-toggle').addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='light'?'dark':'light';theme(value);if(store)store.setTheme(value);});
  if(store){const answers=store.load().lessons[id]?.answers||{};document.querySelectorAll('[data-quiz]').forEach(quiz=>{const saved=answers[quiz.dataset.quiz];const button=[...quiz.querySelectorAll('button')].find(b=>b.dataset.answer===saved);if(button)button.click();});}
  progress();
 }};
})();
