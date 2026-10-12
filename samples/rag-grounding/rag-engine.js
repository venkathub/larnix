/* Original deterministic teaching fixture. No model, embedding or network calls. */
(function (root) {
  'use strict';
  const asOf = '2026-10-12';
  const docs = [
    {id:'R1', title:'Return window · v1', version:'1', from:'2026-01-01', to:'2026-09-30', field:'days', value:7, text:'Standard camera rentals must be returned within 7 calendar days of pickup.'},
    {id:'R2', title:'Return window · v2', version:'2', from:'2026-10-01', to:null, field:'days', value:3, text:'Standard camera rentals must be returned within 3 calendar days of pickup.'},
    {id:'F1', title:'Late fee · v1', version:'1', from:'2026-01-01', to:null, field:'fee', value:200, text:'For standard camera rentals, the late fee is ₹200 for each calendar day beyond the return window.'},
    {id:'H1', title:'Help desk hours · v1', version:'1', from:'2026-01-01', to:null, field:'hours', value:'09:00–18:00', text:'The camera-rental help desk is open from 09:00 to 18:00, Monday to Saturday.'},
    {id:'R3', title:'Return window · conflicting bulletin', version:'1', from:'2026-10-01', to:null, field:'days', value:5, text:'Standard camera rentals must be returned within 5 calendar days of pickup.'}
  ];
  const questions = {
    return:{text:'For a standard camera rental picked up today, what is the return window and daily late fee?', needs:['days','fee'], order:['R1','R2','F1','R3','H1']},
    hours:{text:'What are the camera-rental help desk opening hours?', needs:['hours'], order:['H1','R1','R2','F1','R3']},
    damage:{text:'What is the damage deposit for a standard camera rental?', needs:['deposit'], order:['R1','R2','F1','H1','R3']}
  };
  const defaults = () => ({question:'return', available:['R1','R2','F1','H1'], topK:3, slots:2, currentOnly:true});
  const current = d => d.from <= asOf && (!d.to || asOf <= d.to);
  function run(state) {
    const q = questions[state.question];
    if (!q || !Array.isArray(state.available) || new Set(state.available).size !== state.available.length || state.available.some(id=>!docs.some(d=>d.id===id))) throw new TypeError('Unknown question or document IDs');
    if (![state.topK,state.slots].every(n=>Number.isInteger(n)&&n>=1&&n<=5) || typeof state.currentOnly !== 'boolean') throw new RangeError('Use 1–5 candidates and slots, plus a boolean validity filter');
    // Fixed per-question ordering deliberately exposes a stale high-ranked hit.
    const candidates = q.order.filter(id=>state.available.includes(id)).slice(0,state.topK).map(id=>docs.find(d=>d.id===id));
    const eligible = candidates.filter(d=>!state.currentOnly || current(d));
    const context = eligible.slice(0,state.slots);
    const decisions = candidates.map(d=>({id:d.id,reason:state.currentOnly&&!current(d)?'Excluded: expired on '+d.to:context.includes(d)?'Included in context':'Omitted: context slots full'}));
    const conflicts = q.needs.filter(field=>new Set(context.filter(d=>d.field===field).map(d=>d.value)).size>1);
    const missing = q.needs.filter(field=>!context.some(d=>d.field===field));
    const claims = conflicts.length ? [] : q.needs.flatMap(field=>{
      const matching=context.filter(d=>d.field===field);
      if (!matching.length) return [];
      const value=matching[0].value;
      const text=field==='days'?`The return window is ${value} calendar days from pickup.`:field==='fee'?`The late fee is ₹${value} per calendar day beyond that window.`:`The help desk is open ${value}, Monday to Saturday.`;
      return [{field,text,citations:matching.map(d=>d.id)}];
    });
    const status = conflicts.length?'conflict':missing.length?'abstain':'answer';
    const answer = status==='conflict'?'I found conflicting policy values in the supplied context. Ask the policy owner to resolve them before giving a definitive answer.':status==='abstain'?`I cannot give a complete answer from this context. Missing evidence: ${missing.map(field=>({days:'return window',fee:'daily late fee',hours:'opening hours',deposit:'damage deposit'})[field]).join(', ')}. Retrieve the missing policy or ask the help desk.`:claims.map(c=>c.text+' ['+c.citations.join(', ')+']').join(' ');
    const stale = context.filter(d=>!current(d)).map(d=>d.id);
    return {question:q.text,candidates,context,decisions,claims,missing,conflicts,status,answer,stale};
  }
  const api={asOf,docs,questions,defaults,current,run};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.RagLesson=api;
})(typeof window==='undefined'?globalThis:window);
