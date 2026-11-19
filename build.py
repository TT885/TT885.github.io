#!/usr/bin/env python3
"""Build the two public pages from content/*.md; Python standard library only.

Supported Markdown: paragraphs, **bold**, *italic*, links, images, - lists,
## sections, ### publication titles, and two-column tables. Front matter is
a small key: value configuration block, not a full YAML parser.
"""
import argparse
import html
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import sys
from functools import partial

ROOT = Path(__file__).resolve().parent


def esc(value):
    return html.escape(str(value), quote=True)


def inline(text):
    # Tokenize links before emphasis so underscores inside URLs stay untouched.
    tokens = []
    def link(match):
        label, url = match.groups()
        if not re.match(r'^(https?://|mailto:|#|[\w./-])', url):
            raise ValueError('Unsupported link: ' + url)
        tokens.append('<a href="' + esc(url) + '">' + inline(label) + '</a>')
        return '\x00' + str(len(tokens) - 1) + '\x00'
    text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, text)
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    for number, value in enumerate(tokens):
        text = text.replace('\x00' + str(number) + '\x00', value)
    return text


def read_page(filename):
    text = (ROOT / 'content' / filename).read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(filename + ': missing front matter')
    _, front, body = text.split('---', 2)
    meta = {}
    for line in front.strip().splitlines():
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip()
    sections = {}
    current = None
    for line in body.strip().splitlines():
        if line.startswith('## '):
            current = line[3:].strip()
            if current in sections:
                raise ValueError('Duplicate section: ' + current)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
        elif line.strip():
            raise ValueError('Put text under a ## section')
    return meta, {key: '\n'.join(value).strip() for key, value in sections.items()}


def markdown(text):
    out = []
    for block in re.split(r'\n\s*\n', text.strip()):
        if not block:
            continue
        lines = block.splitlines()
        if all(line.startswith('- ') for line in lines):
            out.append('<ul class="plain-list">' + ''.join('<li>' + inline(line[2:]) + '</li>' for line in lines) + '</ul>')
        elif all(line.startswith('|') and line.endswith('|') for line in lines):
            rows = [[cell.strip() for cell in line.strip('|').split('|')] for line in lines]
            if len(rows) < 3 or any(len(row) != 2 for row in rows):
                raise ValueError('Use a two-column table with a header and separator')
            if not all(re.fullmatch(r':?-+:?', cell) for cell in rows[1]):
                raise ValueError('Table separator must contain dashes')
            out.append('<dl class="stats-grid">' + ''.join('<div class="stat"><dt>' + inline(key) + '</dt><dd>' + inline(value) + '</dd></div>' for key, value in rows[2:]) + '</dl>')
        elif all(re.fullmatch(r'!\[([^\]]*)\]\(([^\s)]+)\)', line) for line in lines):
            for line in lines:
                alt, url = re.fullmatch(r'!\[([^\]]*)\]\(([^\s)]+)\)', line).groups()
                out.append('<figure class="report-image"><a href="' + esc(url) + '"><img src="' + esc(url) + '" alt="' + esc(alt) + '" loading="lazy"></a><figcaption>' + esc(alt) + '</figcaption></figure>')
        elif len(lines) == 1 and lines[0].startswith('### '):
            out.append('<h3>' + inline(lines[0][4:]) + '</h3>')
        else:
            out.append('<p>' + inline(' '.join(lines)) + '</p>')
    return '\n'.join(out)


def publications(text):
    out = []
    for entry in re.split(r'(?m)^### ', text):
        if not entry.strip():
            continue
        title, body = entry.split('\n', 1)
        blocks = re.split(r'\n\s*\n', body.strip())
        if len(blocks) != 3:
            raise ValueError('Each publication needs: metadata, authors, citation (separated by blank lines)')
        meta, authors, citation = blocks
        meta = inline(meta).replace('<strong>CCF-A</strong>', '<strong class="ccf-label">CCF-A</strong>').replace('<strong>Best Paper Award</strong>', '<strong class="award-label">Best Paper Award</strong>')
        out.append('<article class="publication"><p class="publication-meta">' + meta + '</p><h3>' + inline(title) + '</h3><p class="authors">' + inline(authors) + '</p><p class="citation">' + inline(citation) + '</p></article>')
    return '\n'.join(out)


def gallery(text):
    cards = []
    for entry in re.split(r'(?m)^### ', text):
        if not entry.strip():
            continue
        title, body = entry.split('\n', 1)
        cards.append('<article class="gallery-card"><h3>' + inline(title) + '</h3>' + markdown(body) + '</article>')
    return '<div class="gallery-grid">' + '\n'.join(cards) + '</div>'


def head(title, description, url, portrait, outdoor=False):
    return '<!doctype html>\n<html lang="' + ('zh-CN' if outdoor else 'en') + '">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + esc(title) + '</title>\n<meta name="description" content="' + esc(description) + '">\n<meta property="og:title" content="' + esc(title) + '">\n<meta property="og:description" content="' + esc(description) + '">\n<meta property="og:type" content="website">\n<meta property="og:url" content="' + esc(url) + '">\n<meta property="og:image" content="' + esc(url.rsplit('/', 1)[0] + '/' + portrait) + '">\n<link rel="canonical" href="' + esc(url) + '">\n<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n<link rel="stylesheet" href="assets/site.css">\n</head>\n'


def header(outdoor=False):
    return '<body' + (' class="outdoor-page"' if outdoor else '') + '><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="./">' + ('Outdoors' if outdoor else 'Academic homepage') + '</a><nav aria-label="Main navigation"><a href="./"' + ('' if outdoor else ' aria-current="page"') + '>Academic</a><a href="outdoors.html"' + (' aria-current="page"' if outdoor else '') + '>Outdoors · 户外</a></nav></div></header>\n'


def build():
    meta, sections = read_page('academic.md')
    outside, outdoor_sections = read_page('outdoors.md')
    mapping = {'About me': 'about', 'Publications': 'publications', 'Research software': 'projects', 'Education': 'education', 'Honors': 'awards', 'Experience': 'experience'}
    if set(sections) != set(mapping) | {'Keywords'}:
        raise ValueError('Keep the academic ## section names; edit their content freely')
    for key in ('portrait', 'site_url', 'name', 'name_zh', 'email', 'role', 'graduation', 'university', 'location', 'scholar', 'description', 'updated'):
        if not meta.get(key):
            raise ValueError('Missing academic metadata: ' + key)
    for path in (meta['portrait'], outside['portrait']):
        if not (ROOT / path).is_file():
            raise ValueError('Portrait does not exist: ' + path)
    links = [('Google Scholar', meta['scholar'])]
    profile = '<aside class="profile" aria-label="Profile"><div class="portrait academic-portrait"><img src="' + esc(meta['portrait']) + '" alt="Portrait of ' + esc(meta['name']) + '" fetchpriority="high"></div><h1>' + esc(meta['name']) + ' <span lang="zh-CN">' + esc(meta['name_zh']) + '</span></h1><p class="profile-role">' + esc(meta['role']) + '</p><p class="profile-graduation">' + esc(meta['graduation']) + '</p><p class="profile-university">' + esc(meta['university']) + '</p><p class="profile-location">' + esc(meta['location']) + '</p><div class="profile-links">' + ''.join('<a href="' + esc(url) + '">' + esc(label) + '</a>' for label, url in links) + '</div></aside>'
    body = []
    for title, anchor in mapping.items():
        text = sections[title]
        content = publications(text) if anchor == 'publications' else markdown(text)
        if anchor == 'about':
            keywords = [line[2:] for line in sections['Keywords'].splitlines() if line.startswith('- ')]
            content += '<div class="research-topics">' + ''.join('<span>' + inline(word) + '</span>' for word in keywords) + '</div>'
        body.append('<section id="' + anchor + '"><div class="section-heading"><h2>' + esc(title) + '</h2></div>' + content + '</section>')
    footer = '<footer class="page-footer"><span>Updated ' + esc(meta['updated']) + '</span><span>Archive: <a href="projects/">Projects</a> · <a href="lectures/">Lectures</a> · <a href="readings/">Reading</a></span></footer>'
    academic = head(meta['name'] + ' · ' + meta['name_zh'], meta['description'], meta['site_url'] + '/', meta['portrait']) + header() + '<div class="academic-layout">' + profile + '<main id="main">' + '\n'.join(body) + footer + '</main></div></body></html>\n'
    intro = outdoor_sections.pop('Introduction')
    outdoor = head('户外 · Outdoors | ' + meta['name_zh'], outside['description'], meta['site_url'] + '/outdoors.html', outside['portrait'], True) + header(True)
    outdoor += '<main id="main" class="outdoor-main"><section class="outdoor-hero"><div class="outdoor-intro"><h1>' + esc(outside['title']).replace('|', '<br>') + '</h1>' + markdown(intro) + '</div><div class="portrait outdoor-portrait"><img src="' + esc(outside['portrait']) + '" alt="张嘉乐的户外形象照" fetchpriority="high"></div></section>'
    for number, (title, text) in enumerate(outdoor_sections.items()):
        anchor = 'races' if number == 0 else 'outdoor-' + str(number)
        content = gallery(text) if title in ('Race highlights', 'Selected routes') else markdown(text)
        outdoor += '<section class="outdoor-section" id="' + anchor + '"><div class="section-heading"><h2>' + esc(title) + '</h2></div>' + content + '</section>'
    outdoor += '<footer class="page-footer"><a href="./">学术主页 · Academic</a></footer></main></body></html>\n'
    for filename, content in (('index.html', academic), ('outdoors.html', outdoor)):
        target = ROOT / filename
        if not target.exists() or target.read_text(encoding='utf-8') != content:
            target.write_text(content, encoding='utf-8')
        print('Built ' + filename)


def main():
    parser = argparse.ArgumentParser(description='从 Markdown 生成个人主页；--serve 本地预览；--publish 生成、提交并推送。')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--serve', action='store_true')
    group.add_argument('--publish', action='store_true')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    build()
    if args.serve:
        class PreviewHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path.split('?', 1)[0] in ('/', '/index.html', '/outdoors.html'):
                    try:
                        build()
                    except (ValueError, OSError) as error:
                        self.send_error(500, 'Markdown build failed: ' + str(error))
                        return
                super().do_GET()
        print('Preview: http://localhost:' + str(args.port) + '/ — 保存 Markdown 后刷新浏览器即可更新。', flush=True)
        try:
            ThreadingHTTPServer(('localhost', args.port), partial(PreviewHandler, directory=str(ROOT))).serve_forever()
        except KeyboardInterrupt:
            print('\nPreview stopped.')
    if args.publish:
        # Stage only site sources and generated pages; leave unrelated edits alone.
        paths = ['content', 'build.py', 'README.md', 'index.html', 'outdoors.html', 'assets/site.css', 'assets/profile', 'assets/outdoors', '.nojekyll']
        subprocess.run(['git', 'add', '--'] + paths, cwd=ROOT, check=True)
        changed = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT)
        if changed.returncode == 1:
            subprocess.run(['git', '-c', 'user.name=TT885', '-c', 'user.email=' + read_page('academic.md')[0]['email'], 'commit', '-m', 'Update personal homepage from Markdown'], cwd=ROOT, check=True)
        elif changed.returncode != 0:
            raise RuntimeError('Unable to inspect staged changes')
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=ROOT, check=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('Build failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
