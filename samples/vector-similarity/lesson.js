(function () {
  'use strict';
  const M = window.VectorMath;
  const $ = id => document.getElementById(id);
  const defaults = () => ({q: [1, 0], a: [1, 0], b: [2, 2]});
  let vectors = defaults(), metric = 'dot', normalized = false, selected = 'b';
  let projectionVisible = false;
  const svg = $('vector-plot');
  const names = {q: 'Query q', a: 'Document A', b: 'Document B'};
  const symbols = {q: '◆', a: '●', b: '■'};
  const label = key => key === 'q' ? 'q' : key.toUpperCase();
  const fmt = (value, places = 3) => value === null ? 'undefined' : (Math.abs(value) < 0.0000001 ? '0' : Number(value.toFixed(places)).toString());
  const vectorText = v => `(${v.map(x => fmt(x, 2)).join(', ')})`;
  const effective = key => normalized ? M.normalize(vectors[key]) : vectors[key];
  const scale = () => normalized ? 128 : 64;
  const point = v => [250 + v[0] * scale(), 250 - v[1] * scale()];
  function node(tag, attributes = {}, content) {
    const n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attributes).forEach(([k, v]) => n.setAttribute(k, v));
    if (content !== undefined) n.textContent = content;
    return n;
  }
  function draw() {
    const grid = $('plot-grid'); grid.replaceChildren();
    const ticks = normalized ? [-1, 0, 1] : [-3, -2, -1, 0, 1, 2, 3];
    ticks.forEach(v => {
      const p = 250 + v * scale();
      grid.append(node('line', {x1:p, y1:35, x2:p, y2:465, class:v === 0 ? 'axis-line' : 'grid-line'}));
      grid.append(node('line', {x1:35, y1:p, x2:465, y2:p, class:v === 0 ? 'axis-line' : 'grid-line'}));
      if (v !== 0) {
        grid.append(node('text', {x:p, y:483, 'text-anchor':'middle', class:'tick-text'}, v));
        grid.append(node('text', {x:25, y:250 - v * scale() + 6, 'text-anchor':'end', class:'tick-text'}, v));
      }
    });
    svg.querySelector('.unit-circle').setAttribute('r', scale());
    const group = $('plot-vectors'); group.replaceChildren();
    ['q','a','b'].forEach(key => {
      const v = effective(key);
      if (!v) {
        group.append(node('text', {x:260, y:290 + (key === 'q' ? 0 : key === 'a' ? 18 : 36), class:'vector-text', fill:`var(--${key === 'q' ? 'query' : key})`}, `${label(key)}: no direction`));
        return;
      }
      const [x,y] = point(v), color = `var(--${key === 'q' ? 'query' : key})`;
      group.append(node('line', {x1:250,y1:250,x2:x,y2:y,stroke:color,class:'vector-line','stroke-dasharray':key === 'q' ? '6 5' : 'none','marker-end':M.norm(v) ? `url(#arrow-${key})` : ''}));
      if (key === selected) group.append(node('circle', {cx:x,cy:y,r:14,fill:'none',stroke:color,'stroke-opacity':'.5','stroke-width':1}));
      if (key === 'b') group.append(node('rect',{x:x-4,y:y-4,width:8,height:8,fill:color}));
      else if (key === 'q') group.append(node('path',{d:`M${x} ${y-6}l6 6 -6 6 -6 -6z`,fill:color}));
      else group.append(node('circle',{cx:x,cy:y,r:4,fill:color}));
      let labelY = y + (key === 'q' ? 25 : key === 'a' ? -18 : -12);
      labelY = Math.max(24, Math.min(478, labelY));
      group.append(node('text',{x:Math.min(x+12,458),y:labelY,class:'vector-text',fill:color},label(key)));
    });
    const proj = $('plot-projection'); proj.replaceChildren();
    const q = effective('q'), b = effective('b');
    if (projectionVisible && q && b) {
      const projected = M.projection(b, q);
      if (projected) {
        const [x,y] = point(projected), [bx,by] = point(b);
        proj.append(node('line',{x1:bx,y1:by,x2:x,y2:y,class:'projection-line'}));
        proj.append(node('line',{x1:250,y1:250,x2:x,y2:y,class:'projection-line'}));
        proj.append(node('circle',{cx:x,cy:y,r:5,fill:'var(--surface)',stroke:'var(--b)'}));
      }
    }
    $('plot-desc').textContent = `Query ${vectorText(vectors.q)}, document A ${vectorText(vectors.a)}, document B ${vectorText(vectors.b)}. ${normalized ? 'Nonzero vectors shown normalized to unit length.' : 'Raw vectors shown.'} ${projectionVisible ? 'Projection overlay shows B onto q, where defined.' : ''} Use coordinate fields for a keyboard alternative.`;
    svg.style.cursor = normalized ? 'default' : 'crosshair';
  }
  function render(updateFields = true, announce = false) {
    $('metric-dot').setAttribute('aria-pressed', metric === 'dot');
    $('metric-cosine').setAttribute('aria-pressed', metric === 'cosine');
    $('normalize').checked = normalized;
    $('show-projection').checked = projectionVisible;
    document.querySelectorAll('[data-vector]').forEach(b => b.setAttribute('aria-pressed', b.dataset.vector === selected));
    $('plot-mode').textContent = normalized ? 'Unit vectors · 2× zoom' : 'Raw vectors';
    $('drag-help').textContent = normalized ? 'Normalized view. Edit raw coordinates below, or turn normalization off to drag.' : 'Drag to change raw coordinates. The faint circle marks unit length.';
    if (updateFields) ['q','a','b'].forEach(k => {$(k+'x').value=vectors[k][0];$(k+'y').value=vectors[k][1];});
    const ranked = ['a','b'].map(key => ({key, value:M.score(vectors.q,vectors[key],metric,normalized)})).sort((a,b) => a.value === null ? (b.value === null ? 0 : 1) : b.value === null ? -1 : b.value-a.value);
    const valid = ranked.filter(x => x.value !== null);
    const tie = valid.length === 2 && Math.abs(valid[0].value-valid[1].value) < 1e-10;
    $('winner').textContent = !valid.length ? 'No valid cosine direction' : tie ? 'A and B tie' : `${label(valid[0].key)} ranks first`;
    if (!valid.length && metric === 'dot') $('winner').textContent = 'Cannot normalize zero';
    let explanation;
    if (!valid.length) explanation = 'The query or both documents have zero length. An undefined score is not a zero score.';
    else if (valid.length === 1) explanation = `${label(valid[0].key)} is the only valid candidate. The other document has no direction and is excluded from this ranking.`;
    else if (tie) explanation = `The ${metric === 'dot' ? 'dot products' : 'cosine similarities'} are equal. Keep the tie explicit; neither document wins on this metric.`;
    else if (metric === 'cosine' || normalized) explanation = `${label(valid[0].key)} aligns more closely with q. Positive vector length does not affect this comparison.`;
    else explanation = `${label(valid[0].key)} has the larger dot product with q. The score reflects both alignment and vector magnitude.`;
    $('vector-inputs').textContent = `Raw arrows: q=${vectorText(vectors.q)} · A=${vectorText(vectors.a)} · B=${vectorText(vectors.b)}`;
    $('vector-scores').textContent = `${metric === 'dot' ? (normalized ? 'Normalized dot' : 'Dot') : 'Cosine'} scores: A = ${fmt(M.score(vectors.q,vectors.a,metric,normalized))} · B = ${fmt(M.score(vectors.q,vectors.b,metric,normalized))}`;
    $('ranking-explanation').textContent = explanation;
    $('vector-nearby-result').textContent = `${$('winner').textContent}. ${explanation}`;
    $('rank-list').replaceChildren();
    ranked.forEach((item,index) => {
      const li=document.createElement('li');
      const order=document.createElement('span');order.textContent=item.value === null ? '—' : tie ? '1 =' : String(index+1);
      const name=document.createElement('span');name.className=item.key+'-color';name.textContent=`${symbols[item.key]} ${names[item.key]}`;
      const score=document.createElement('span');score.className='score'+(item.value === null ? ' undefined' : '');score.textContent=fmt(item.value);
      li.append(order,name,score);$('rank-list').append(li);
    });
    const q=effective('q'), d=effective(selected === 'q' ? 'b' : selected), name=selected === 'q' ? 'B' : label(selected);
    const result=M.score(vectors.q,vectors[selected === 'q' ? 'b' : selected],metric,normalized);
    $('formula-label').textContent=`${metric === 'dot' ? 'DOT PRODUCT' : 'COSINE'} · q WITH ${name}`;
    if (!q || !d) $('live-formula').textContent = 'Zero length → normalization undefined';
    else if (metric === 'dot') $('live-formula').textContent=`${fmt(q[0])} × ${fmt(d[0])} + ${fmt(q[1])} × ${fmt(d[1])} = ${fmt(result)}`;
    else $('live-formula').textContent=`${fmt(M.dot(q,d))} / (${fmt(M.norm(q))} × ${fmt(M.norm(d))}) = ${fmt(result)}`;
    $('formula-note').textContent = result === null ? 'Undefined values are excluded, never silently replaced with 0.' : 'Displayed values are rounded; ranking uses full precision.';
    draw();
    if (announce) $('lab-announcement').textContent = `${$('winner').textContent}. ${explanation} A: ${fmt(M.score(vectors.q,vectors.a,metric,normalized))}. B: ${fmt(M.score(vectors.q,vectors.b,metric,normalized))}.`;
  }
  ['dot','cosine'].forEach(value => $('metric-'+value).addEventListener('click',() => {metric=value;render(false,true);}));
  $('normalize').addEventListener('change',e => {normalized=e.target.checked;render(false,true);});
  $('show-projection').addEventListener('change',e => {projectionVisible=e.target.checked;render(false,true);});
  document.querySelectorAll('[data-vector]').forEach(button => button.addEventListener('click',() => {selected=button.dataset.vector;render(false);}));
  ['q','a','b'].forEach(key => ['x','y'].forEach((axis,i) => {
    const input=$(key+axis);
    input.addEventListener('input',() => {
      const value=input.valueAsNumber;
      if (!Number.isFinite(value) || value < -3 || value > 3) {$('input-error').textContent='Enter a finite coordinate between −3 and 3. The graph retains the last valid value.';return;}
      vectors[key][i]=value;selected=key;
      $('input-error').textContent='';render(false);
    });
    function commitCoordinate() {
      if (!Number.isFinite(input.valueAsNumber) || input.valueAsNumber < -3 || input.valueAsNumber > 3) input.value=vectors[key][i];
      $('input-error').textContent='';render(false,true);
    }
    input.addEventListener('change',commitCoordinate);
    input.addEventListener('blur',commitCoordinate);
  }));
  let dragging=false;
  function movePointer(e) {
    const rect=svg.getBoundingClientRect();
    // The SVG preserves a square viewBox even if its CSS box is rectangular.
    const side=Math.min(rect.width,rect.height), left=rect.left+(rect.width-side)/2, top=rect.top+(rect.height-side)/2;
    const x=(e.clientX-left)*500/side, y=(e.clientY-top)*500/side;
    const round=value => Math.round(Math.max(-3,Math.min(3,value))*10)/10;
    vectors[selected]=[round((x-250)/64),round((250-y)/64)];
    $('input-error').textContent='';render();
  }
  svg.addEventListener('pointerdown',e => {if (normalized || e.button !== 0) return;dragging=true;svg.setPointerCapture(e.pointerId);movePointer(e);});
  svg.addEventListener('pointermove',e => {if (dragging) movePointer(e);});
  function stopDrag() {if(dragging){dragging=false;render(true,true);}}
  svg.addEventListener('pointerup',stopDrag);svg.addEventListener('pointercancel',stopDrag);
  $('reset').addEventListener('click',() => {vectors=defaults();metric='dot';normalized=false;selected='b';projectionVisible=false;$('input-error').textContent='';render(true,true);});
  function preset(name) {
    vectors=defaults();normalized=false;selected='b';projectionVisible=false;
    if(name==='opposite'){vectors.b=[-2,0];metric='cosine';}
    else if(name==='zero'){vectors.b=[0,0];metric='cosine';}
    else metric='dot';
    $('input-error').textContent='';render(true,true);
  }
  document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click',() => preset(button.dataset.preset)));
  $('try-scale').addEventListener('click',() => {vectors=defaults();vectors.a=[3,0];metric='dot';normalized=false;selected='a';render(true,true);});
  $('try-zero').addEventListener('click',() => {preset('zero');$('experiment').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});$('metric-cosine').focus({preventScroll:true});});
  const questions={
    prediction:{answer:'b',correct:'Yes. q · A = 1, while q · B = 2. B’s larger x component wins under dot product. Cosine will ask a different question.',wrong:'Look at the x component: q = (1, 0) makes the dot product equal to the document’s x value. A scores 1 and B scores 2. Try again.'},
    scale:{answer:'dot',correct:'Exactly. q · A becomes 3. Cosine is 3 / (1 × 3) = 1. Positive scaling changes length, not direction.',wrong:'Multiplying A by 3 also multiplies its length by 3. In cosine those factors cancel; in dot product they do not. Try again.'},
    zero:{answer:'undefined',correct:'Correct. The denominator contains a zero norm, so cosine is undefined. Exclude or quarantine the vector according to an explicit policy.',wrong:'A zero dot product does not rescue a zero denominator. There is no direction to compare, so cosine is undefined. Try again.'}
  };
  window.LessonUI.init({id:'M03-L01',questions});
  const links=[...document.querySelectorAll('.lesson-nav nav a')];
  const observer=new IntersectionObserver(entries => {
    entries.filter(entry=>entry.isIntersecting).forEach(entry => links.forEach(link=>{
      const active=link.hash===`#${entry.target.id}`;
      link.classList.toggle('active',active);
      if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');
    }));
  },{rootMargin:'-10% 0px -60% 0px',threshold:0});
  links.forEach(link=>observer.observe(document.querySelector(link.hash)));
  render();
})();
