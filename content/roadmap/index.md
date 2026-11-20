{
  "title": "学习路线",
  "date": "2026-10-15T11:44:22+08:00",
  "draft": false,
  "description": "从张量与梯度，到优化器、Transformer、LLM 训练和实验基本功。",
  "ShowReadingTime": false
}

沿着一次训练向外展开。以“能解释、能实现、能分析实验”衡量进度，不以读过多少篇笔记衡量。

## 怎么学

先在对话中一次讲清一个小问题，围绕疑问逐步解释，必要时共同手算或讨论代码。随后根据实际对话整理笔记；未讨论的课程和实验不提前撰写或发布。下面是候选路线，具体顺序和深度随讨论调整。

掌握度分为：未开始 → 能解释 → 能推导 → 能实现 → 能分析实验。每次学习后，用自己的话写下理解与疑问；阅读过不等于掌握。

## 01 · 张量与自动求导 {#tensors}

按知识点分别讨论，再整理为独立笔记：

1. [张量与 shape：模型里的数据是什么样的？]({{< relref "/posts/tensors-and-shapes" >}}) · 已讨论并发布
2. [张量运算与广播：能运行，为什么还可能算错？]({{< relref "/posts/tensor-operations-and-broadcasting" >}}) · 已讨论并发布
3. [矩阵乘法与线性层：输入特征怎样变成输出？]({{< relref "/posts/matrix-multiplication-and-linear-layers" >}}) · 已讨论并发布
4. [导数与梯度：怎样描述函数的局部变化？]({{< relref "/posts/derivatives-and-gradients" >}}) · 已讨论并发布
5. [链式法则与计算图：多步计算的导数怎样连接？]({{< relref "/posts/chain-rule-and-computational-graphs" >}}) · 已讨论并发布
6. [反向传播：按什么顺序求导，怎样复用结果？]({{< relref "/posts/backpropagation" >}}) · 已讨论并发布
7. [PyTorch autograd：计算图、梯度与几个容易混淆的开关]({{< relref "/posts/pytorch-autograd" >}}) · 已讨论并发布

- 实践目标：手算一次梯度，识别广播错误，对齐手算与自动求导。

## 02 · 训练与优化 {#optimization}

依赖：01。共九篇，已根据实际讨论整理发布，本章以 AdamW 结束：

1. [从函数到训练：模型究竟在优化什么？]({{< relref "/posts/training-objective" >}}) · 已讨论并发布
2. [梯度下降：怎样完成一次参数更新？]({{< relref "/posts/gradient-descent" >}}) · 已讨论并发布
3. [Mini-batch 与 SGD：为什么不每次用全部数据？]({{< relref "/posts/mini-batch-and-sgd" >}}) · 已讨论并发布
4. [Momentum：为什么更新还需要惯性？]({{< relref "/posts/momentum" >}}) · 已讨论并发布
5. [Adam：为什么不同参数可以有不同的更新尺度？]({{< relref "/posts/adam" >}}) · 已讨论并发布
6. [学习率调度与 warmup：为什么步子要随时间变化？]({{< relref "/posts/learning-rate-scheduling-and-warmup" >}}) · 已讨论并发布
7. [梯度裁剪：更新前为什么要限制梯度？]({{< relref "/posts/gradient-clipping" >}}) · 已讨论并发布
8. [泛化与正则化：训练得更好，为什么不一定预测得更好？]({{< relref "/posts/generalization-and-regularization" >}}) · 已讨论并发布
9. [AdamW：weight decay 为什么需要单独处理？]({{< relref "/posts/adamw" >}}) · 已讨论并发布

实践目标：在相同数据、初始化与预算下比较优化器；解释 AdamW 状态、学习率和 weight decay；诊断 loss 不下降。实践尚未展开。

## 03 · 网络基本组件：从单层计算到完整网络 {#components}

依赖：01、02。共规划 15 篇，按“先搭网络，再理解深层训练，最后衔接文本模型”的顺序讨论。前三篇已根据讨论整理，其余为待讨论主题，未提前撰写课程正文。

每篇围绕四个问题：算了什么、输入输出 shape、哪些量可学习、梯度怎样通过。第一章已讲过的运算只简要回顾。

| 顺序与篇目 | 计划讨论的内容 | 状态 |
| --- | --- | --- |
| 1. [Linear 层：一个输出单元究竟在做什么？]({{< relref "/posts/linear-output-units" >}}) | 输出单元的加权组合、参数共享；输入与权重的梯度汇总，以及平均损失的缩放。 | 已讨论并发布 |
| 2. [激活函数：为什么需要 ReLU、GELU 和 SiLU？]({{< relref "/posts/activation-functions" >}}) | 纯线性层叠加的局限；函数形状、梯度、负值区域与 ReLU 失活；不预设某一种普遍最优。 | 已讨论并发布 |
| 3. [MLP：怎样把层连接成一个网络？]({{< relref "/posts/mlp" >}}) | 输入、隐藏与输出层，宽度与深度；组合 Linear 和激活，追踪小网络的 shape、参数量和前向过程，接回训练流程。 | 已讨论并整理 |
| 4. 分类输出：logits、概率与交叉熵怎样连接？ | 从回归转向二分类、多分类；Sigmoid、Softmax、预测类别、交叉熵与标签形式，为什么接口常接收 logits；先限于单标签分类。 | 待讨论 |
| 5. 卷积层：卷积核滑动时到底算了什么？ | 单通道小矩阵手算；局部连接、滑动窗口、权重共享，与 Linear 的联系，以及图像中的设计动机。 | 待讨论 |
| 6. 多通道卷积：通道、步幅与填充怎样影响结果？ | 输入与输出通道、卷积核 shape；kernel size、stride、padding、输出尺寸和参数量，明确跨通道求和。 | 待讨论 |
| 7. 常见卷积变体：1×1、分组与深度卷积 | 通道混合、groups 改变的连接、深度卷积与逐点卷积的组合，比较计算方式和参数量。 | 待讨论 |
| 8. 池化、感受野与 CNN：怎样从图像得到预测？ | Max／Average Pooling、下采样、感受野；Flatten 与全局平均池化；小 CNN 的尺寸、通道和分类输出。 | 待讨论 |
| 9. 参数初始化：为什么初始权重不能随便设？ | 全零初始化的对称性问题；前向与反向的尺度；Xavier、Kaiming 的动机及与激活函数的关系。 | 待讨论 |
| 10. 残差连接：为什么把输入再加回来？ | y=x+F(x) 的前向含义、shape 对齐、反向路径；帮助深层训练的原因与局限。 | 待讨论 |
| 11. BatchNorm：归一化为什么会有训练与评估两套行为？ | 卷积特征图上的统计范围；均值、方差、ε、可学习缩放与偏移，运行统计和参数的区别。 | 待讨论 |
| 12. LayerNorm：为什么沿特征轴归一化？ | 用 (batch, token, feature) 手算统计范围；与 BatchNorm 对照，参数 shape 及各 token 的独立处理。 | 待讨论 |
| 13. RMSNorm：不减均值，怎样控制数值尺度？ | 均方根、与 LayerNorm 的公式及参数差异，用数值例子区分尺度归一化与中心化。 | 待讨论 |
| 14. Dropout 与模式切换：训练和推理为什么不同？ | 随机掩码、保留概率、缩放；结合 BatchNorm 区分 train()、eval()、no_grad() 和冻结参数。 | 待讨论 |
| 15. Embedding：离散编号怎样变成可学习向量？ | 查表、权重矩阵、输出 shape、重复编号的参数共享与梯度汇总，与 one-hot 加 Linear 的联系。 | 待讨论 |

贯穿本章的内容：

- 张量衔接：在 MLP、CNN 中讨论 reshape、Flatten、permute，区分换轴与改变 shape。
- 组件顺序：熟悉各组件后，用具体例子比较归一化、激活与残差的排列，不预设唯一模板。
- 状态与参数：区分梯度更新的参数、模型保存的其他状态，以及训练／评估时的行为。

小 MLP、CNN 和代码同样先在对话中讨论，再按确认后的内容整理。通常每篇阅读 5～7 分钟，复杂主题随实际讨论调整。本章实践尚未展开。

## 04 · Transformer 与注意力 {#transformer}

依赖：01、03。学习 tokenization、embedding、Q/K/V、scaled dot-product attention、causal mask、多头注意力、位置编码与 RoPE。

实践目标：从张量形状写出小型 causal self-attention，检查 mask 是否泄漏未来信息，拼出小 Transformer。章节尚未展开。

## 05 · LLM 的训练过程 {#llm-training}

依赖：02、04。学习数据清洗与去重、token budget、next-token prediction、label shift、padding/loss mask、预训练、SFT、偏好优化（DPO 与基于奖励的路线）、评估与数据污染。

实践目标：解释每个阶段的数据、训练目标和更新参数；跑通一个小语言模型的训练、验证、保存和恢复。章节尚未展开。

## 06 · 效率、显存与训练系统 {#systems}

依赖：02、04；LLM 案例依赖 05。学习参数/梯度/优化器状态/激活的内存开销，BF16/FP16、梯度累积、activation checkpointing、GPU 内存层级、DDP 与参数分片概念。

FlashAttention 专题的前置链：**普通 attention → 注意力矩阵的内存开销 → HBM/SRAM 与 IO → 分块 → online softmax → FlashAttention**。再讨论数值误差和测量方式。

实践目标：估算显存，分辨计算与内存瓶颈，在同等条件下测量速度和数值一致性。章节尚未展开。

## 07 · Research 的实验基本功 {#research}

贯穿各阶段，完成 02 后可系统学习。内容包括 baseline、公平比较、消融、多个随机种子、指标与不确定性、实验配置、复现与排错日志。

实践目标：用一个小实验写出“问题—假设—对照—结果—局限”，把观察和解释分开。章节尚未展开。

## 两条复习路径

**训练排错路径：** shape → loss 定义 → 梯度 → 参数更新 → 数据与评估 → 数值稳定性。

**读论文路径：** 解决什么问题 → 改了哪个环节 → 依赖什么假设 → 如何实现 → 用什么证据支持 → 在什么情况下可能失效。
