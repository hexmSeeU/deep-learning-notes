# deep-learning-notes

面向 research 的中文深度学习基础笔记。参照 [aigc-notes](https://github.com/hexmSeeU/aigc-notes) 的组织方式，采用 **Hugo 0.150.1 extended + PaperMod + GitHub Pages**。

从一次训练出发，系统学习张量与梯度、优化器、网络组件、Transformer、LLM 训练、FlashAttention 与实验基本功。每课包含直觉、必要推导、最小实现、对照实验和自检。

仓库：[hexmSeeU/deep-learning-notes](https://github.com/hexmSeeU/deep-learning-notes)。网站地址：`https://hexmSeeU.github.io/deep-learning-notes/`。首次需在仓库 Settings → Pages 中选择 GitHub Actions，发布工作流成功后网站才会上线。

## 目录

```text
content/
  posts/how-neural-networks-learn/  第一课 page bundle：正文与代码下载
  roadmap/                        七个模块的学习路线
  review/                         自测与复习方法
  archives.md                     文章归档
  search.md                       全站搜索
archetypes/posts/index.md          新课程模板
examples/                         可独立运行的实验
static/js/                        交互实验及数值引擎
assets/css/extended/               阅读与实验样式
layouts/                          首页与教学 shortcode
scripts/                          主题准备、正文与链接检查
tests/                            梯度与跨语言数值验证
.github/workflows/pages.yml        main → 检查 → Hugo → Pages
```

## 本地预览

安装 Hugo **0.150.1 extended**；检查脚本使用 Python 3.10+，跨语言数值验证使用 Node。网站构建无 npm/pip 依赖，PyTorch 只是可选实验依赖。

```sh
bash scripts/prepare-theme.sh
hugo server --buildDrafts
```

若本地已有完整的无 Git 元数据的主题缓存，可以直接 `hugo server`；干净克隆后运行主题准备脚本即可。

## 写一篇新课

```sh
hugo new content posts/tensors-and-shapes/index.md
```

正文保存在 `content/posts/<slug>/index.md`，图片与可下载代码可放同一 page bundle。填写模板中的 JSON front matter；真实发布日期需带时区，`lastmod` 仅在实质更新时修改。发布前把 `draft` 设为 `false`。

同仓库页面用 Hugo `relref` 链接，资源使用相对路径，适配 GitHub Pages 项目子路径。公式块可用 `equation` shortcode 展示 Unicode 公式；当前没有引入 TeX 渲染库。

文章按“问题 → 直觉 → 推导 → 实现 → 实验 → 边界”展开，参考资料与后续阅读置于“小结与自检”之前。自检答案紧跟问题直接展示。复制实验到文章目录后运行检查，确保下载版与 `examples/` 保持同步。

公开仓库的草稿和 Git 历史也公开，私人学习记录请保存在仓库之外。

## 验证

```sh
python -m unittest discover -s tests -v
python scripts/check_content.py
hugo --minify --cleanDestinationDir
python scripts/check_site.py
python examples/first_training.py --lr 0.1 --steps 100
# 可选：已安装 torch 时
python examples/first_training_torch.py
```

## GitHub Pages 首次发布

1. 在 GitHub 创建空仓库 `hexmSeeU/deep-learning-notes`，不要初始化 README 或其他文件。
2. 推送本目录的 `main` 分支：

   ```sh
   git remote add origin https://github.com/hexmSeeU/deep-learning-notes.git
   git push -u origin main
   ```

3. 仓库 **Settings → Pages → Source** 选择 **GitHub Actions**。如首次工作流早于设置而失败，在 Actions 中重新运行 `Publish learning notes`。
4. 成功部署后访问 `https://hexmSeeU.github.io/deep-learning-notes/`。以后更新 `main` 自动检查和发布；回退使用 `git revert`。

## 当前进度

七个模块的路线已经建立。第一课《一个神经网络究竟是怎么学会东西的？》含手算、Python/PyTorch、交互实验与自检；其他课程后续逐课编写。
