#!/usr/bin/env bash
set -euo pipefail
# 与参考仓库使用相同的 PaperMod 版本。
commit=d3768854d00ad003b0a8dbdba254ce9224377a01
if [ ! -d themes/PaperMod/.git ]; then
  if [ -e themes/PaperMod ]; then
    echo 'themes/PaperMod exists without Git metadata. Keep it for local preview, or move it aside before fetching the pinned theme.' >&2
    exit 1
  fi
  git clone https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
fi
git -C themes/PaperMod checkout --detach "$commit"
