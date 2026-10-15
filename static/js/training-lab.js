(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  if (!$('training-lab')) return;
  const E = window.TrainingEngine;
  const lab = $('training-lab');
  lab.className = 'lab';
  lab.innerHTML = `<p class="lab-title">实验台 / 看见一次学习</p><p class="lab-description">数据 (0,1)、(1,3)、(2,5) · 初始 w=b=0 · L=mean((ŷ−y)²)/2</p><div class="lab-controls"><label>学习率 η <select id="lr"><option value="0">0</option><option value="0.01">0.01</option><option selected value="0.1">0.1</option><option value="0.5">0.5</option><option value="1">1.0</option></select></label><button id="step-one">更新 1 步</button><button id="step-many">更新 10 步</button><button id="reset-lab">重置</button></div><div class="lab-stats"><div><span>更新次数</span><b id="stat-step"></b></div><div><span>权重 w</span><b id="stat-w"></b></div><div><span>偏置 b</span><b id="stat-b"></b></div><div><span>损失 L</span><b id="stat-loss"></b></div></div><svg id="fit-plot" class="plot" viewBox="0 0 560 205" role="img" aria-label="目标数据与当前模型预测线"></svg><p class="plot-legend">● 训练数据　 ··· 目标关系 y=2x+1　 — 当前预测（超出范围会裁剪）</p><svg id="loss-plot" class="plot" viewBox="0 0 560 160" role="img" aria-label="训练 loss 随更新次数变化的曲线"></svg><p id="lab-status" class="lab-status" role="status" aria-live="polite"></p>`;
  let state, history, count;
  const fmt = n => Math.abs(n) >= 10000 ? n.toExponential(2) : n.toFixed(4);
  function reset() { state = E.evaluate(0, 0); history = [state.loss]; count = 0; draw(); }
  function advance(n) {
    for (let i = 0; i < n && count < 200; i++) {
      const next = E.next(state, Number($('lr').value));
      if (!Number.isFinite(next.loss) || next.loss > 1e12) break;
      state = next; history.push(state.loss); count++;
    }
    draw();
  }
  function draw() {
    $('stat-step').textContent = count; $('stat-w').textContent = fmt(state.w); $('stat-b').textContent = fmt(state.b); $('stat-loss').textContent = fmt(state.loss);
    const xp = x => 45 + x*210, yp = y => 175-y*26;
    const pred = [0, 2].map(x => `${xp(x)},${yp(Math.max(-10, Math.min(15, state.w*x+state.b)))}`).join(' ');
    $('fit-plot').innerHTML = `<defs><clipPath id="plot-clip"><rect x="35" y="10" width="455" height="177"/></clipPath></defs><path class="axis" d="M35 10V187H490"/><text x="500" y="190">x</text><text x="12" y="20">y</text><text x="40" y="201">0</text><text x="250" y="201">1</text><text x="460" y="201">2</text><text x="16" y="150">1</text><text x="16" y="98">3</text><text x="16" y="46">5</text><g clip-path="url(#plot-clip)"><path class="target" d="M${xp(0)} ${yp(1)}L${xp(2)} ${yp(5)}"/><polyline class="prediction" points="${pred}"/>${E.data.map(([x,y]) => `<circle class="point" cx="${xp(x)}" cy="${yp(y)}" r="4"/>`).join('')}</g>`;
    const max = Math.max(...history, 0.0001);
    const points = history.map((l,i) => `${45+i*440/Math.max(count,1)},${125-l/max*100}`).join(' ');
    $('loss-plot').innerHTML = `<path class="axis" d="M35 15V130H490"/><text x="0" y="15">Loss</text><text x="40" y="148">0</text><text x="450" y="148">step ${count}</text><text x="42" y="20">上界 ${fmt(max)}</text><polyline class="prediction" points="${points}"/><circle class="point" r="3" cx="${45+count*440/Math.max(count,1)}" cy="${125-state.loss/max*100}"/>`;
    let message = count === 0 ? '先预测：执行一次更新，w、b 和 loss 会怎样变化？' : `当前梯度：dw=${fmt(state.dw)}，db=${fmt(state.db)}。`;
    const stopped = count >= 200 || state.loss > 1e10;
    if (state.loss > 1e10) message = 'loss 已急剧增大，实验已暂停。重置后尝试更小的学习率。';
    else if (count >= 200) message += ' 已达到 200 步，可重置后比较另一组学习率。';
    else if (count > 0 && Number($('lr').value) === 0) message += ' 学习率为零，参数保持不变。';
    $('lab-status').textContent = message;
    $('step-one').disabled = stopped; $('step-many').disabled = stopped;
  }
  $('step-one').addEventListener('click', () => advance(1));
  $('step-many').addEventListener('click', () => advance(10));
  $('reset-lab').addEventListener('click', reset);
  $('lr').addEventListener('change', reset);
  reset();
})();
