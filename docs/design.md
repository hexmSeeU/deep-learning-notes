# 项目约定

本项目参照 hexmSeeU/aigc-notes，使用独立 GitHub 仓库 deep-learning-notes，Hugo + PaperMod 构建并通过 GitHub Pages 发布。

学习主线：数据 → 前向 → loss → 反向 → 更新 → 评估。路线分为七个模块；课程只在完成正文、最小实现与自测之后作为正式文章发布。

内容保存在 content/posts/<slug>/index.md。读者入口为首页、路线、文章、复习、归档与搜索。第一课保留无后端的浏览器参数更新实验，与 Python 共用目标函数与数据。

依赖：Hugo 0.150.1 extended；PaperMod 固定到 d3768854d00ad003b0a8dbdba254ce9224377a01，与参考仓库一致。Python/Node 仅用于检查，PyTorch 为可选学习实验。

CI 检查正文、梯度、JavaScript/Python 一致性，再验证根路径与 /deep-learning-notes/ 两种产物链接。只将 public/ 部署至 Pages。
