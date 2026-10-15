"""验证 Hugo 产物在根路径和 GitHub Pages 项目子路径下的站内链接。"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'link' and attrs.get('rel') in ('canonical', 'alternate'):
            return
        for field in ('href', 'src'):
            if attrs.get(field):
                self.refs.append(attrs[field])


def check(directory='public', base='https://hexmSeeU.github.io/deep-learning-notes/'):
    root = Path(directory).resolve()
    base_url = urlsplit(base)
    prefix = base_url.path
    pages = {p.resolve(): Page(p.read_text()) for p in root.rglob('*.html')}
    for path in ('index.html', 'roadmap/index.html', 'posts/index.html', 'review/index.html'):
        assert (root / path) in pages, f'Required framework page missing: {path}'
    count = 0
    for file, page in pages.items():
        path = file.relative_to(root).as_posix()
        url = urljoin(base, path[:-10] if path.endswith('index.html') else path)
        for ref in page.refs:
            parsed = urlsplit(urljoin(url, ref))
            if parsed.netloc != base_url.netloc or parsed.scheme not in ('https', 'http'):
                continue
            decoded = unquote(parsed.path)
            assert decoded.startswith(prefix), f'{file}: path escapes Pages prefix: {ref}'
            target = (root / decoded[len(prefix):]).resolve()
            if target.is_dir():
                target /= 'index.html'
            assert target.is_relative_to(root), f'{file}: escaped output: {ref}'
            assert target.exists(), f'{file}: broken link: {ref}'
            if parsed.fragment and target in pages:
                assert unquote(parsed.fragment) in pages[target].ids, f'{file}: missing anchor: {ref}'
            count += 1
    print(f'Checked {len(pages)} HTML pages and {count} local links/anchors for {base}: OK')


if __name__ == '__main__':
    check(*sys.argv[1:])
