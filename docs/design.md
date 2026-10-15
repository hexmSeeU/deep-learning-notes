# 项目约定

本项目采用独立 GitHub 仓库 deep-learning-notes，Hugo + PaperMod 构建，通过 GitHub Pages 发布。

用户的学习方式优先：先逐步讲解并讨论，再根据对话内容整理笔记。网站当前只保留框架和候选路线；未讨论的课程、实验与自测不预写或发布。具体约定见 AGENTS.md。

未来笔记保存在 content/posts/<slug>/index.md。读者入口包括首页、路线、文章、复习、归档和搜索。课程列表为空是正常初始状态。

Hugo 固定为 0.150.1 extended，PaperMod 固定为 d3768854d00ad003b0a8dbdba254ce9224377a01。Python 仅用于内容与链接检查。CI 验证根路径和 /deep-learning-notes/ 子路径，部署产物为 public/。
