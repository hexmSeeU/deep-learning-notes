/* 与 examples/first_training.py 相同的数据、目标和全批量梯度。 */
(function (root) {
  'use strict';
  const data = [[0, 1], [1, 3], [2, 5]];
  function evaluate(w, b) {
    let loss = 0, dw = 0, db = 0;
    data.forEach(([x, y]) => { const e = w*x+b-y; loss += e*e/6; dw += e*x/3; db += e/3; });
    return {w, b, loss, dw, db};
  }
  function next(state, lr) {
    return evaluate(state.w - lr*state.dw, state.b - lr*state.db);
  }
  const api = {data, evaluate, next};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.TrainingEngine = api;
})(typeof window !== 'undefined' ? window : globalThis);
