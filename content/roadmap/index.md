{
  "title": "学习路线",
  "date": "2026-10-15T11:44:22+08:00",
  "draft": false,
  "description": "从张量与梯度，到优化器、Transformer、LLM 训练和实验基本功。",
  "ShowReadingTime": false
}

沿着一次训练向外展开。以“能解释、能实现、能分析实验”衡量进度，不以读过多少篇笔记衡量。

## 怎么学

每课建议分三轮：先读直觉和例子，再运行或修改实验，最后不看答案完成自测。时长取决于基础，不设赶进度的周计划。遇到数学缺口就地补齐。

掌握度分为：未开始 → 能解释 → 能推导 → 能实现 → 能分析实验。每次学习后，用自己的话写下理解与疑问；阅读过不等于掌握。

## 01 · 张量与自动求导

**现在从这里开始。** 先贯通训练，再补计算语言。

- 第 01 课：[一个神经网络究竟是怎么学会东西的？]({{< relref "/posts/how-neural-networks-learn" >}}) · 已有完整讲解与实验
- 第 02 课：张量、shape、广播与矩阵乘法 · 待编写
- 第 03 课：导数、链式法则、计算图与 autograd · 待编写
- 实践目标：手算一次梯度，识别广播错误，对齐手算与自动求导。

## 02 · 训练与优化

依赖：01。学习 loss、mini-batch、epoch/step、SGD、Momentum、Adam、AdamW、学习率调度、warmup、梯度裁剪、正则化与泛化。

实践目标：在相同数据、初始化与预算下比较优化器；解释 AdamW 状态、学习率和 weight decay；诊断 loss 不下降。章节尚未展开。

## 03 · 网络基本组件

依赖：01、02。学习初始化、ReLU/GELU/SiLU、残差连接、LayerNorm、RMSNorm、dropout 与训练/评估模式。

实践目标：追踪梯度范数，比较不同初始化，解释残差和归一化的作用及局限。章节尚未展开。

## 04 · Transformer 与注意力

依赖：01、03。学习 tokenization、embedding、Q/K/V、scaled dot-product attention、causal mask、多头注意力、位置编码与 RoPE。

实践目标：从张量形状写出小型 causal self-attention，检查 mask 是否泄漏未来信息，拼出小 Transformer。章节尚未展开。

## 05 · LLM 的训练过程

依赖：02、04。学习数据清洗与去重、token budget、next-token prediction、label shift、padding/loss mask、预训练、SFT、偏好优化（DPO 与基于奖励的路线）、评估与数据污染。

实践目标：解释每个阶段的数据、训练目标和更新参数；跑通一个小语言模型的训练、验证、保存和恢复。章节尚未展开。

## 06 · 效率、显存与训练系统

依赖：02、04；LLM 案例依赖 05。学习参数/梯度/优化器状态/激活的内存开销，BF16/FP16、梯度累积、activation checkpointing、GPU 内存层级、DDP 与参数分片概念。

FlashAttention 专题的前置链：**普通 attention → 注意力矩阵的内存开销 → HBM/SRAM 与 IO → 分块 → online softmax → FlashAttention**。再讨论数值误差和测量方式。

实践目标：估算显存，分辨计算与内存瓶颈，在同等条件下测量速度和数值一致性。章节尚未展开。

## 07 · Research 的实验基本功

贯穿各阶段，完成 02 后可系统学习。内容包括 baseline、公平比较、消融、多个随机种子、指标与不确定性、实验配置、复现与排错日志。

实践目标：用一个小实验写出“问题—假设—对照—结果—局限”，把观察和解释分开。章节尚未展开。

## 两条复习路径

**训练排错路径：** shape → loss 定义 → 梯度 → 参数更新 → 数据与评估 → 数值稳定性。

**读论文路径：** 解决什么问题 → 改了哪个环节 → 依赖什么假设 → 如何实现 → 用什么证据支持 → 在什么情况下可能失效。
