/* Hand-checkable local calculations for the mathematical notebook experiments. */
(function(root){
 'use strict';
 function step(weight,rate){
  if(!Number.isFinite(weight)||!Number.isFinite(rate)||rate<0||rate>1.5)throw new RangeError('Finite weight and rate in [0, 1.5] required');
  const gradient=2*(weight-3),next=weight-rate*gradient;
  return {before:weight,gradient,weight:next,loss:(next-3)**2};
 }
 function threshold(cutoff){
  if(!Number.isFinite(cutoff)||cutoff<0||cutoff>1)throw new RangeError('Threshold must be in [0, 1]');
  const scores=[.9,.8,.7,.4,.3,.1],labels=[1,0,1,1,0,0];
  const predictions=scores.map(s=>s>=cutoff),reviewed=predictions.filter(Boolean).length;
  const tp=predictions.reduce((n,p,i)=>n+(p&&labels[i]?1:0),0);
  return {scores,labels,predictions,reviewed,tp,fp:reviewed-tp,fn:3-tp,precision:reviewed?tp/reviewed:null,recall:tp/3};
 }
 const api={step,threshold};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.FoundationMath=api;
})(typeof window==='undefined'?globalThis:window);
