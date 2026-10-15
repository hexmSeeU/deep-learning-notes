# deep-learning-notes

面向 research 的中文深度学习基础学习笔记，参照 [aigc-notes](https://github.com/hexmSeeU/aigc-notes)，使用 Hugo 0.150.1 extended + PaperMod + GitHub Pages。

## 学习方式

先在对话中一次讲清一个问题，围绕疑问逐步解释，必要时共同讨论手算和代码。再根据实际对话整理笔记。尚未讨论的课程和实验不提前写入或发布。

《张量与 shape》《张量运算与广播》和《矩阵乘法与线性层》三篇笔记已根据对话整理发布。后续主题继续先讨论再整理，不预写课程或实验。

## 目录

- `content/posts/`：根据实际讨论整理的笔记。
- `content/roadmap/`：候选学习路线。
- `content/review/`：以后根据讨论整理的复习内容，当前仅说明。
- `archetypes/posts/index.md`：文章格式模板。
- `layouts/`、`assets/`、`static/`：网站布局与样式。
- `data/learning.toml`：首页候选学习地图，与路线页保持一致。
- `docs/hero-artwork.md`：首页 AI 插画的提示词、来源与导出尺寸。
- `scripts/`：主题准备、正文和链接检查。
- `.github/workflows/pages.yml`：main 分支的检查和 Pages 发布。

## 本地预览与检查

安装 Hugo **0.150.1 extended**；检查脚本使用 Python 3.10+。网站无 npm/pip 依赖。

```sh
bash scripts/prepare-theme.sh
hugo server --buildDrafts
```

若已有无 Git 元数据的主题缓存，可直接运行 Hugo；干净克隆后运行主题准备脚本。

```sh
python scripts/check_content.py
hugo --minify --cleanDestinationDir
python scripts/check_site.py
```

## 整理笔记

只有对应内容已经在对话中讲解和讨论后，才新建 `content/posts/<slug>/index.md`。填写带时区的真实日期、标题、摘要与标签；草稿设为 `draft: true`。使用 `relref` 处理站内链接。

参考资料和后续阅读放在“小结与自检”之前。若讨论中需要自检，答案紧跟问题展示。模板中的章节按实际对话内容填写，不为凑齐模板预写课程。

公开仓库的草稿及 Git 历史也公开，私人记录请保存在仓库之外。

## 发布

仓库：[hexmSeeU/deep-learning-notes](https://github.com/hexmSeeU/deep-learning-notes)。首次在 Settings → Pages 将 Source 设为 GitHub Actions。之后 main 更新触发工作流，成功后可访问 `https://hexmSeeU.github.io/deep-learning-notes/`。
