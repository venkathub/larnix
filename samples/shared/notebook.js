/* Draw each explanatory sketch once as it enters view; content remains visible without JS. */
(function(){
 'use strict';
 if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const observer=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('ink-visible');observer.unobserve(entry.target);}});
 },{threshold:.2});
 document.querySelectorAll('.concept-sketch').forEach(sketch=>observer.observe(sketch));
})();
