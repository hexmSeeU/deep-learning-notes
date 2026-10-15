"""检查文章元数据、收尾规范与实验下载文件是否同步。"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decoder = json.JSONDecoder()
posts = list((ROOT / 'content/posts').glob('*/index.md'))
assert posts, 'No lesson posts found'
for p in posts:
    text = p.read_text()
    meta, end = decoder.raw_decode(text)
    for field in ('title', 'description', 'date', 'slug', 'categories', 'tags', 'draft'):
        assert field in meta, f'{p}: missing {field}'
    date = datetime.fromisoformat(meta['date'])
    assert date.tzinfo is not None, f'{p}: date needs timezone'
    assert date <= datetime.now(date.tzinfo), f'{p}: future publication date'
    body = text[end:]
    headings = re.findall(r'^## (.+)$', body, re.M)
    assert headings[-1].endswith('小结与自检'), f'{p}: final section must be self-check'
    assert '<details>' not in body, f'{p}: answers should appear directly after questions'
    assert not re.search(r'\]\((?!https?://)[^)]*\.html\)', body), f'{p}: old static page links'
for name in ('first_training.py', 'first_training_torch.py'):
    assert (ROOT / 'examples' / name).read_bytes() == (ROOT / 'content/posts/how-neural-networks-learn' / name).read_bytes(), f'Outdated download: {name}'
print(f'Checked {len(posts)} post(s), metadata, closing sections and code downloads: OK')
