"""Validate public conference data and render a standalone, no-service DDL page."""
import hashlib
import html
import json
from datetime import date, datetime
from urllib.parse import urlparse


def esc(value):
    return html.escape(str(value), quote=True)


def validate(data):
    date.fromisoformat(data['checked'])
    ids = set()
    for conf in data['conferences']:
        if conf['id'] in ids:
            raise ValueError('Duplicate conference: ' + conf['id'])
        ids.add(conf['id'])
        if conf['area'] not in data['areas']:
            raise ValueError('Unknown area: ' + conf['area'])
        date.fromisoformat(conf['checked'])
        for source in conf['sources']:
            if urlparse(source['url']).scheme != 'https':
                raise ValueError('Sources must be HTTPS')
        for cycle in conf['cycles']:
            for key in ('abstract', 'paper'):
                value = cycle.get(key)
                if value is None:
                    continue
                if bool(value.get('at')) == bool(value.get('date')):
                    raise ValueError('Use exactly one of at or date')
                if value.get('at'):
                    dt = datetime.fromisoformat(value['at'].replace('Z', '+00:00'))
                    if dt.utcoffset() is None:
                        raise ValueError('Deadline must include UTC offset')
                else:
                    date.fromisoformat(value['date'])
                if not value.get('original'):
                    raise ValueError('Keep original source timezone/date')
            abstract, paper = cycle.get('abstract'), cycle.get('paper')
            if abstract and paper and abstract.get('at') and paper.get('at'):
                if datetime.fromisoformat(abstract['at']) > datetime.fromisoformat(paper['at']):
                    raise ValueError('Abstract is after full paper: ' + conf['id'])


def build_deadlines(root, site_url):
    data = json.loads((root / 'content/deadlines.json').read_text(encoding='utf-8'))
    validate(data)
    def version(path):
        return hashlib.sha256((root / path).read_bytes()).hexdigest()[:10]
    # JSON is inert page data. Escaping '<' also prevents accidental </script>.
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    fallback = []
    for conf in data['conferences']:
        rows = []
        for cycle in conf['cycles']:
            deadlines = []
            for key, label in [('abstract', '摘要'), ('paper', '全文')]:
                value = cycle.get(key)
                deadlines.append(label + '：' + esc(value['original'] if value else '未公布 / 未单列'))
            rows.append('<li>' + esc(cycle['label']) + ' — ' + '；'.join(deadlines) + '</li>')
        sources = ' · '.join('<a href="' + esc(s['url']) + '">' + esc(s['label']) + '</a>' for s in conf['sources'])
        fallback.append('<article class="conference"><h2>' + esc(conf['name']) + ' ' + str(conf['edition']) + '</h2><p>' + esc(conf['note']) + '</p><ul>' + ''.join(rows) + '</ul><p>' + sources + '</p></article>')
    areas = ''.join('<button type="button" data-area="' + esc(key) + '" aria-pressed="false">' + esc(value) + '</button>' for key, value in data['areas'].items())
    page = f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Conference deadlines · Jiale Zhang</title>
<meta name="description" content="My conference deadline watchlist: data systems, mobile computing, networks and machine learning. Official sources, submission cycles and timezone conversion.">
<link rel="canonical" href="{esc(site_url)}/ddls/">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/site.css?v={version('assets/site.css')}">
<link rel="stylesheet" href="../assets/deadlines.css?v={version('assets/deadlines.css')}">
<script src="../assets/deadlines.js?v={version('assets/deadlines.js')}" defer></script>
</head><body class="deadlines-page">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="wordmark" href="../">Academic homepage</a><nav aria-label="Main navigation"><a href="../">Academic</a><a href="../outdoors.html">Outdoors · 户外</a><a href="./" aria-current="page">DDL</a></nav></div></header>
<main id="main" class="ddl-main">
<section class="ddl-intro"><h1>Conference deadlines<span>会议投稿日历</span></h1>
<p>数据系统、移动计算与网络、机器学习。只跟踪主会研究论文；先看摘要，再看全文。</p>
<div class="ddl-summary"><span><strong>{len(data['conferences'])}</strong> 个会议</span><span id="live-counts">官方来源核对：{esc(data['checked'])}</span><span id="today"></span></div></section>
<section class="ddl-controls" aria-label="筛选与显示设置">
<div class="filter-row" id="area-filters" role="group" aria-label="按方向筛选"><button type="button" data-area="all" aria-pressed="true">全部方向</button>{areas}</div>
<div class="control-row"><label class="search-label">搜索会议<input id="search" type="search" placeholder="ICDE, VLDB, MobiCom…" autocomplete="off"></label>
<label>投稿状态<select id="status"><option value="all">全部状态</option><option value="upcoming">仍有投稿窗口</option><option value="pending">日期待公布</option><option value="closed">本届已截止</option></select></label>
<label>显示时区<select id="timezone"><option value="Asia/Shanghai">北京时间 · UTC+8</option><option value="UTC">UTC</option><option value="local">我的设备时区</option></select></label>
<button type="button" id="reset" class="reset">重置</button></div>
</section>
<aside class="ddl-notice"><strong>以官方 CFP 为准。</strong> 已公布的精确时刻可自动换算；仅有日期的保留原时区，不补造时分。AoE = UTC−12。倒计时随设备时钟变化，<strong>会议数据不自动联网更新</strong>。<span>最近核对：{esc(data['checked'])} · <a href="../content/deadlines.json">查看数据源</a></span></aside>
<p class="results-label" id="results-label" role="status" aria-live="polite"></p>
<div id="conference-list"></div><p id="empty-state" hidden>没有匹配的会议。试试清空搜索或切换筛选。</p>
<noscript><p>JavaScript 未启用：以下显示原始日期与官方入口，不提供实时状态。核对日期 {esc(data['checked'])}。</p>{''.join(fallback)}</noscript>
<footer class="ddl-footer"><p>Personal watchlist · 仅包含公开会议信息，不记录稿件、投稿计划或私人申请资料。</p><p>参考 <a href="https://weihao-cui.com/ddls/">Weihao Cui's DDL page</a> · 日期见各会议官方来源。<a href="../">返回学术主页</a></p></footer>
</main><script id="conference-data" type="application/json">{payload}</script></body></html>
'''
    target = root / 'ddls/index.html'
    target.parent.mkdir(exist_ok=True)
    if not target.exists() or target.read_text(encoding='utf-8') != page:
        target.write_text(page, encoding='utf-8')
    print('Built ddls/index.html (' + str(len(data['conferences'])) + ' conferences)')
