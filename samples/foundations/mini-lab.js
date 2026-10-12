(function(){
 'use strict';
 const id=window.FoundationLesson.id,M=window.FoundationMath,$=id=>document.getElementById(id);
 const fmt=x=>Number.isFinite(x)?Number(x.toFixed(4)).toString():'outside this toy range';
 const node=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
 if(id==='M04-L03'){
  function render(){const cutoff=Number($('threshold-input').value),s=M.threshold(cutoff);$('threshold-value').textContent=fmt(cutoff);
   $('live-result').textContent=`${s.reviewed} reviews · ${s.tp} true alerts · ${s.fp} false alerts · ${s.fn} missed urgent. Precision ${s.precision===null?'undefined (no alerts)':fmt(s.precision)}; recall ${fmt(s.recall)}.`;
   $('score-tickets').replaceChildren(...s.scores.map((score,i)=>{const card=node('li');card.dataset.flag=String(s.predictions[i]);card.append(node('strong',`Ticket ${i+1} · ${score}`),node('span',s.labels[i]?'Actually urgent':'Actually routine'),node('span',s.predictions[i]?'→ Review':'→ No review'));return card;}));
  }
  $('threshold-input').addEventListener('input',render);render();
 }else if(id==='M03-L02'||id==='M05-L02'){
  let weight=0,steps=0;
  function render(message){
   $('live-result').textContent=message||`Start: w = 0, loss = 9. Choose a rate, then take one step.`;
   const within=weight>=-3&&weight<=9, x=45+(weight+3)*30, y=230-Math.pow(weight-3,2)*5;
   $('descent-point').setAttribute('cx',x);$('descent-point').setAttribute('cy',y);$('descent-point').style.display=within?'':'none';
   $('descent-desc').textContent=`Loss is (w−3) squared. Minimum at w=3, loss=0. Current weight ${fmt(weight)}, loss ${fmt((weight-3)**2)}.${within?'':' The point is outside the shown chart range.'}`;
   $('step-learning').disabled=steps>=8;$('descent-range').textContent=within?'Chart shows w from −3 to 9. Minimum: (3, 0).':'The point left the chart; read the exact weight and loss above. Reset to start again.';
  }
  function reset(){weight=0;steps=0;render();}
  $('step-learning').addEventListener('click',()=>{const s=M.step(weight,Number($('rate-input').value));weight=s.weight;steps++;render(`Step ${steps}: ${fmt(s.before)} − ${$('rate-input').value} × (${fmt(s.gradient)}) → w = ${fmt(weight)}. Loss = ${fmt(s.loss)}.${steps>=8?' Eight-step limit reached; reset to compare another rate.':''}`);});
  $('reset-learning').addEventListener('click',reset);$('rate-input').addEventListener('change',reset);render();
 }
})();
