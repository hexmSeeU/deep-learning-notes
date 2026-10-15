"""检查已有笔记；讨论开始前允许没有课程文章。"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decoder = json.JSONDecoder()
posts = list((ROOT / 'content/posts').glob('*/index.md'))
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
    assert headings and headings[-1].endswith('小结与自检'), f'{p}: final section must be self-check'
    assert '<details>' not in body, f'{p}: answers should appear directly after questions'
    assert not re.search(r'\]\((?!https?://)[^)]*\.html\)', body), f'{p}: old static page links'
print(f'Checked {len(posts)} post(s), metadata and closing sections: OK (no posts is allowed)')
