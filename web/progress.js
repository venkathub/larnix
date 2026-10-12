/* Versioned local-only learner state. No tracking or network requests. */
(function(root){
 'use strict';
 const KEY='larnix.progress.v1';
 const empty=()=>({version:1,lessons:{},theme:'dark',lastLesson:null});
 function clean(input){
  const data=empty();
  if(!input||input.version!==1||typeof input.lessons!=='object'||!input.lessons)return data;
  data.theme=input.theme==='light'?'light':'dark';
  const validId=id=>/^M\d{2}-L\d{2}$/.test(id);
  for(const [id,entry] of Object.entries(input.lessons)){
   if(!validId(id)||!entry||typeof entry!=='object')continue;
   const answers={};
   if(entry.answers&&typeof entry.answers==='object')for(const [key,value] of Object.entries(entry.answers))if(/^[a-z][a-z0-9_-]{0,40}$/.test(key)&&typeof value==='string'&&value.length<=80)answers[key]=value;
   data.lessons[id]={read:entry.read===true,exercise:entry.exercise===true,bookmarked:entry.bookmarked===true,answers};
  }
  data.lastLesson=typeof input.lastLesson==='string'&&validId(input.lastLesson)?input.lastLesson:null;
  return data;
 }
 function create(storage){
  let memory=empty(),persistent=true;
  function load(){if(!persistent)return clean(memory);try{const raw=storage.getItem(KEY);memory=raw?clean(JSON.parse(raw)):empty();}catch{persistent=false;}return clean(memory);}
  function save(next){memory=clean(next);try{storage.setItem(KEY,JSON.stringify(memory));}catch{persistent=false;}return loadMemory();}
  const loadMemory=()=>clean(memory);
  function update(id,patch){if(!/^M\d{2}-L\d{2}$/.test(id))throw new TypeError('Invalid lesson ID');const data=persistent?load():loadMemory();data.lessons[id]={read:false,exercise:false,bookmarked:false,answers:{},...data.lessons[id],...patch};return save(data);}
  return {load:()=>persistent?load():loadMemory(),update,reset:()=>save(empty()),setTheme:theme=>save({...load(),theme}),visit:id=>{const data=load();data.lastLesson=id;return save(data);},isPersistent:()=>persistent};
 }
 const api={KEY,clean,create};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 else{let storage;try{storage=root.localStorage;}catch{storage={getItem(){throw Error('Storage unavailable');},setItem(){throw Error('Storage unavailable');}};}root.LarnixProgress=create(storage);}
})(typeof window==='undefined'?globalThis:window);
