# 验证与发布状态

2026-10-15：按参考仓库迁移到 Hugo 0.150.1 extended + PaperMod。

- Hugo 默认构建成功，第一课正常生成。
- 根站点与 GitHub Pages 项目子路径各检查 20 个 HTML 页面、280 项站内资源/链接/锚点，通过。
- 4 项数值测试通过，覆盖手算、梯度数值差分、学习率行为、浏览器/Python 一致性。
- 文章元数据、带时区的非未来日期、最后章节为小结与自检、代码下载副本同步，检查通过。
- JavaScript 语法检查通过。
- 未进行真实浏览器渲染验收。

目标为 hexmSeeU/deep-learning-notes 与 GitHub Pages。用户已创建公开远程仓库，首次上传沿用 main。Pages 首次启用需在仓库 Settings → Pages 选择 GitHub Actions；工作流状态以仓库 Actions 为准。

先前误用的 Sites 配置已移出当前项目；原版备份位于 /tmp/deep-learning-notes-before-hugo。当前版本只维护 Hugo/GitHub Pages 发布链路。
