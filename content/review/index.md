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

之后根据我们的实际讨论，逐步记录讲清楚的问题、仍然困惑的地方，以及值得回顾的例子。私人学习记录请保存在公开仓库之外。
