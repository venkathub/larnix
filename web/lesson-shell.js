(function(){
 'use strict';
 const id=document.documentElement.dataset.platformLesson,D=window.LarnixData,P=window.LarnixProgress,shell=document.getElementById('course-shell');
 const lesson=D.modules.flatMap(m=>m.lessons).find(l=>l.id===id);
 const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n;};
 const a=(text,url)=>{const n=el('a',text);n.href=url;return n;};
 const root='../../';
 P.visit(id);
 const links=el('nav');links.className='course-links';links.setAttribute('aria-label','Course navigation');links.append(a('← Curriculum',root+'#/catalog'),a('Lesson plan & prerequisites',root+'#/lesson/'+id),a('My progress',root+'#/progress'));shell.append(links);
 const tools=el('details'),toolsTitle=el('summary','Progress & navigation');tools.className='course-tools';tools.append(toolsTitle);shell.append(tools);
 const actions=el('div');actions.className='course-actions';
 const saved=P.load().lessons[id]||{};
 const bookmark=el('button',saved.bookmarked?'Bookmarked ✓':'Bookmark lesson');bookmark.type='button';bookmark.setAttribute('aria-pressed',String(!!saved.bookmarked));bookmark.addEventListener('click',()=>{const value=!P.load().lessons[id]?.bookmarked;P.update(id,{bookmarked:value});bookmark.textContent=value?'Bookmarked ✓':'Bookmark lesson';bookmark.setAttribute('aria-pressed',String(value));});actions.append(bookmark);
 for(const [key,title] of [['read','I have read this lesson'],['exercise','I have practiced the exercise']]){const label=el('label'),input=el('input');input.type='checkbox';input.checked=saved[key]===true;input.addEventListener('change',()=>P.update(id,{[key]:input.checked}));label.append(input,document.createTextNode(title));actions.append(label);}
 tools.append(actions);
 const note=el('p',P.isPersistent()?'Saved on this browser. Check answers restore on return; reading and practice are self-reported, not a mastery score.':'Browser storage is unavailable. Progress lasts only while this page remains open.');note.className='progress-explanation';tools.append(note);
 const nav=el('div');nav.className='lesson-neighbors';const order=D.order.flatMap(mid=>D.modules.find(m=>m.id===mid).lessons),position=order.findIndex(l=>l.id===id);
 const destination=l=>D.previews[l.id]?root+'lessons/'+l.id+'/':root+'#/lesson/'+l.id;
 const suffix=l=>D.previews[l.id]?'':' (plan)';
 if(position>0){const previous=order[position-1];nav.append(a('← '+previous.id+' · '+previous.title+suffix(previous),destination(previous)));}
 if(order[position+1]){const next=order[position+1];nav.append(a(next.id+' · '+next.title+suffix(next)+' →',destination(next)));}tools.append(nav);
 const completion=document.querySelector('.completion');
 if(completion){const continuation=nav.cloneNode(true);continuation.setAttribute('aria-label','Continue learning');completion.after(continuation);}
 const brand=document.querySelector('.topbar .brand');brand.href=root;brand.setAttribute('aria-label','Larnix home');
 // Fixed curriculum navigation stays outside the lesson's own section anchors.
})();
