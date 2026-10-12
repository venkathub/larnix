(function(root){
 'use strict';
 function search(modules,{query='',track='',availability='all',view='learn',previews={},bookmarked=[],tracks=[]}={}){
  const terms=query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const trackIds=track?tracks.find(t=>t.id===track)?.modules||[]:null;
  return modules.flatMap(module=>{
   if(trackIds&&!trackIds.includes(module.id))return [];
   const lessons=module.lessons.filter(lesson=>{
    if(availability==='interactive'&&!previews[lesson.id])return false;
    if(availability==='planned'&&previews[lesson.id])return false;
    if(availability==='bookmarked'&&!bookmarked.includes(lesson.id))return false;
    const fields=[module.id,module.title,lesson.id,lesson.title,...lesson.topics,lesson.outcome];
    if(view==='interview')fields.push(lesson.interview.question,...lesson.interview.strong_answer_signals);
    if(view==='production')fields.push(lesson.production_exercise.brief,...lesson.production_exercise.acceptance);
    const text=fields.join(' ').toLowerCase();return terms.every(term=>text.includes(term));
   });
   return lessons.length?[{...module,lessons}]:[];
  });
 }
 function correctChecks(entry,preview){return Object.entries(preview?.answers||{}).filter(([key,answer])=>entry?.answers?.[key]===answer).length;}
 const api={search,correctChecks};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.LarnixCatalog=api;
})(typeof window==='undefined'?globalThis:window);
