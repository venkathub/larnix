/* Original, deterministic teaching model. No network, storage or real refunds. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.RecoveryEngine=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 const defaults={crash:'commit',policy:'safe',lookupOnline:true,payloadChanged:false};
 const clone=x=>JSON.parse(JSON.stringify(x));
 function config(input={}){
  const c={...defaults,...input};
  if(!['before','commit','receipt','saved'].includes(c.crash)||!['blind','safe'].includes(c.policy)||typeof c.lookupOnline!=='boolean'||typeof c.payloadChanged!=='boolean')throw new TypeError('Invalid recovery configuration');
  return c;
 }
 // The fictional provider atomically records the effect and the key→receipt mapping.
 // It never expires keys in this simulation. This is an assumption, not a client guarantee.
 function commit(state,key,amount){
  const existing=state.ledger.find(r=>r.key===key);
  if(existing){if(existing.amount!==amount)throw new Error('Key reused with different parameters');return clone(existing);}
  const receipt={id:'receipt-'+(state.ledger.length+1),key,amount,currency:'INR',rental:'R-104'};
  state.ledger.push(receipt);return clone(receipt);
 }
 function submit(state,key,amount){state.calls++;return commit(state,key,amount);}
 function recover(input,options={}){
  const c=config(options),s=clone(input);
  s.memoryReceipt=null;
  if(s.checkpoint.status==='done'){
   s.status='complete';s.event='Resume from the saved receipt. No tool call is needed.';return s;
  }
  const amount=c.payloadChanged?700:500;
  if(c.policy==='safe'){
   if(amount!==s.checkpoint.amount){s.status='blocked';s.event='STOP: the retry amount differs from the durable intent. Reconcile the original action; authorize any new action separately.';return s;}
   if(!c.lookupOnline){s.status='held';s.event='HOLD: receipt lookup is unavailable. Unknown does not mean absent. Keep the original operation ID for later reconciliation.';return s;}
   const receipt=s.ledger.find(r=>r.key===s.checkpoint.key);
   if(receipt&&['amount','currency','rental'].some(field=>receipt[field]!==s.checkpoint[field])){
    s.status='blocked';s.event='STOP: the provider receipt does not match the saved intent. Investigate before claiming completion.';return s;
   }
   s.memoryReceipt=receipt?clone(receipt):submit(s,s.checkpoint.key,amount);
   s.event=receipt?'Receipt found for the original operation. Save it without submitting again.':'Authoritative lookup found no receipt. Submit the original intent with the same key; save the returned receipt.';
  }else{
   s.memoryReceipt=submit(s,'retry-'+s.calls,amount);
   s.event='No local completion record: blindly submit under a fresh key, then save this new receipt.';
  }
  s.checkpoint={...s.checkpoint,status:'done',receipt:clone(s.memoryReceipt)};
  s.status=s.ledger.length>1?'duplicate':s.memoryReceipt.amount!==s.checkpoint.amount?'incorrect':'complete';
  return s;
 }
 function run(options={}){
  const c=config(options),frames=[];
  let s={checkpoint:{version:1,status:'pending',key:'refund-R104-01',amount:500,currency:'INR',rental:'R-104',receipt:null},memoryReceipt:null,ledger:[],calls:0,status:'running',event:''};
  function snapshot(event,status='running'){s.event=event;s.status=status;frames.push(clone(s));}
  snapshot('Save the authorized intent and operation ID before calling the tool.');
  if(c.crash!=='before'){
   s.calls++;snapshot('Dispatch the request. A sent request is not yet a completion record.');
   const receipt=commit(s,s.checkpoint.key,500);
   snapshot('The provider commits one ₹500 effect and retains its receipt. The agent has not received the response.');
   if(c.crash!=='commit'){
    s.memoryReceipt=receipt;snapshot('The receipt arrives in process memory. It is not yet in the durable checkpoint.');
    if(c.crash==='saved'){
     s.checkpoint={...s.checkpoint,status:'done',receipt:clone(receipt)};snapshot('Save the receipt and completion status in the checkpoint.');
    }
   }
  }
  s.memoryReceipt=null;snapshot('CRASH: process memory disappears. The checkpoint and provider ledger survive.','crashed');
  s=recover(s,c);frames.push(clone(s));
  return {config:c,frames,result:s};
 }
 return {defaults,run,recover};
});
