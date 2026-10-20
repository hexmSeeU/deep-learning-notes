{
  "title": "复习与学习记录",
  "description": "根据实际讨论逐步积累复习内容。",
  "draft": false,
  "ShowReadingTime": false
}

[第一篇：张量与 shape]({{< relref "/posts/tensors-and-shapes" >}}) 已根据讨论整理。复习时先确认每个轴的含义，再检查索引或切片后的 shape；文末保留了讨论中用过的自检问题。

[第二篇：张量运算与广播]({{< relref "/posts/tensor-operations-and-broadcasting" >}}) 已根据讨论整理。重点回顾：右对齐不等于长度必须相等、`keepdim` 如何配合广播，以及为什么最后得到标量也不能证明 loss 算对了。

[第三篇：矩阵乘法与线性层]({{< relref "/posts/matrix-multiplication-and-linear-layers" >}}) 已根据讨论整理。重点回顾：行列点积、PyTorch weight 的转置约定、最后一轴的特征变换、参数共享与参数量，以及线性层叠加的表达边界。

[第四篇：导数与梯度]({{< relref "/posts/derivatives-and-gradients" >}}) 用普通函数串起变化率、偏导数与梯度。重点回顾局部近似、负梯度方向，以及为什么零梯度不能直接证明函数值最小。

[第五篇：链式法则与计算图]({{< relref "/posts/chain-rule-and-computational-graphs" >}}) 继续使用普通函数。重点回顾路径内相乘、同一输入的路径贡献相加、独立输入分别求导，以及共享节点如何避免漏算。

[第六篇：反向传播]({{< relref "/posts/backpropagation" >}}) 重点回顾反向计算的依赖顺序、共享节点的贡献汇总，以及同一个中间导数如何供多个输入复用。求导本身不会修改输入值。

[第七篇：PyTorch autograd]({{< relref "/posts/pytorch-autograd" >}}) 重点区分前向记录、反向执行和梯度保存。结合计算图回顾 grad_fn、叶子与非叶子、梯度累加、no_grad 与 detach，以及 retain_grad、retain_graph、create_graph 的不同作用。第一章七篇笔记已根据讨论整理完成。

[第二章 · 第一篇：从函数到训练]({{< relref "/posts/training-objective" >}}) 用房价预测串起参数、标签与平均损失。重点回顾：整体损失下降不要求每条样本都改善；训练目标、评价指标与泛化表现需要分别判断。

[第二章 · 第二篇：梯度下降]({{< relref "/posts/gradient-descent" >}}) 从手算更新到最小训练循环。重点回顾学习率与调整量、backward 与 step、no_grad 与 zero_grad，以及参数更新后为什么必须重新前向。

[第二章 · 第三篇：Mini-batch 与 SGD]({{< relref "/posts/mini-batch-and-sgd" >}}) 重点区分 batch size、更新 step、epoch 和有效 batch size；回顾 shuffle 如何保持样本配对，以及梯度累积为何要按样本数加权。

[第二章 · 第四篇：Momentum]({{< relref "/posts/momentum" >}}) 重点回顾独立保存的动量状态、历史贡献的衰减，以及累积形式与平均形式的尺度差异。固定 β 时，累积形式学习率等于平均形式学习率乘 (1−β)。

[第二章 · 第五篇：Adam]({{< relref "/posts/adam" >}}) 重点回顾一阶矩记录方向趋势、二阶矩记录平方尺度、零初始化的偏差修正，以及 ε 和完整更新流程。区分当前梯度、优化器状态与实际调整量。

[第二章 · 第六篇：学习率调度与 warmup]({{< relref "/posts/learning-rate-scheduling-and-warmup" >}}) 回顾分段与余弦衰减、warmup 和偏差修正的区别。重点检查阶段进度与计数单位：梯度累积时，按更新次数的调度应跟实际参数更新同步。

[第二章 · 第七篇：梯度裁剪]({{< relref "/posts/gradient-clipping" >}}) 区分整体范数与逐元素裁剪、裁剪范围，以及裁剪梯度与降低学习率的区别。梯度累积时，先正确汇总本次更新的梯度，再统一裁剪一次。

之后根据我们的实际讨论，逐步记录讲清楚的问题、仍然困惑的地方，以及值得回顾的例子。私人学习记录请保存在公开仓库之外。
