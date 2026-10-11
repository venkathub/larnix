/* Original, dependency-free arithmetic shared by the lesson and its tests. */
(function (root) {
  'use strict';
  function validate(v) {
    if (!Array.isArray(v) || !v.length || !v.every(Number.isFinite)) {
      throw new TypeError('A vector must be a nonempty array of finite numbers.');
    }
  }
  function pair(a, b) {
    validate(a); validate(b);
    if (a.length !== b.length) throw new RangeError('Vector dimensions must match.');
  }
  function dot(a, b) { pair(a, b); return a.reduce((sum, x, i) => sum + x * b[i], 0); }
  function norm(v) { validate(v); return Math.hypot(...v); }
  function normalize(v) { const n = norm(v); return n === 0 ? null : v.map(x => x / n); }
  function cosine(a, b) {
    pair(a, b);
    const ua = normalize(a), ub = normalize(b);
    return ua && ub ? Math.max(-1, Math.min(1, dot(ua, ub))) : null;
  }
  function projection(v, onto) {
    pair(v, onto);
    const unit = normalize(onto);
    return unit ? unit.map(x => x * dot(v, unit)) : null;
  }
  function score(q, d, metric, normalizeFirst = false) {
    pair(q, d);
    if (!['dot', 'cosine'].includes(metric)) throw new RangeError('Unknown similarity metric.');
    if (normalizeFirst) { q = normalize(q); d = normalize(d); if (!q || !d) return null; }
    return metric === 'dot' ? dot(q, d) : cosine(q, d);
  }
  const api = Object.freeze({ dot, norm, normalize, cosine, projection, score });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VectorMath = api;
})(typeof window === 'undefined' ? globalThis : window);
