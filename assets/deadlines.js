/* No framework, no network requests: content/deadlines.json is embedded at build. */
'use strict';
(() => {
  const data = JSON.parse(document.getElementById('conference-data').textContent);
  const list = document.getElementById('conference-list');
  const search = document.getElementById('search');
  const status = document.getElementById('status');
  const timezone = document.getElementById('timezone');
  let area = 'all';
  const DAY = 86400000;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const localZone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';

  // Date-only bounds classify the calendar day; they are never presented as
  // an official timestamp or used for a precise clock countdown.
  function bounds(value) {
    if (!value) return null;
    if (value.at) return {start: Date.parse(value.at), end: Date.parse(value.at), exact: true};
    const base = Date.parse(value.date + 'T00:00:00Z');
    return value.zone === 'AoE'
      ? {start: base + 12 * 3600000, end: base + 36 * 3600000 - 1, exact: false}
      : {start: base - 14 * 3600000, end: base + 36 * 3600000 - 1, exact: false};
  }
  function state(conf, now) {
    const available = conf.cycles.filter(c => c.paper && bounds(c.paper).end >= now)
      .sort((a, b) => bounds(a.paper).start - bounds(b.paper).start);
    if (available.length) {
      const cycle = available[0];
      const abstract = bounds(cycle.abstract);
      const registeredOnly = !!(abstract && abstract.end < now);
      const next = cycle.abstract && !registeredOnly ? cycle.abstract : cycle.paper;
      const uncertainTime = !next.at && !next.zone;
      return {status: 'upcoming', cycle, next, nextLabel: cycle.abstract && !registeredOnly ? '摘要截止' : '全文截止', registeredOnly, uncertainTime, sort: bounds(next).start};
    }
    return {status: conf.pending ? 'pending' : 'closed', cycle: null, sort: Infinity};
  }
  function localized(value) {
    if (!value.at) return escape(value.original);
    const zone = timezone.value === 'local' ? localZone : timezone.value;
    const parts = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
      timeZone: zone, year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'
    }).formatToParts(new Date(value.at)).map(p => [p.type, p.value]));
    return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}`;
  }
  function timeCell(value, label, now, missing) {
    if (!value) return `<div><span class="deadline-label">${label}</span><span class="deadline-unavailable">${escape(missing || '未公布 / 未单列')}</span></div>`;
    const expired = bounds(value).end < now;
    const zone = timezone.value === 'local' ? localZone : timezone.value;
    const zoneLabel = zone === 'Asia/Shanghai' ? '北京时间' : zone;
    const detail = value.at ? `${zoneLabel} · 原始：${value.original}` : '仅日期 · 原时区保留，未补造时分';
    return `<div${expired ? ' class="expired"' : ''}><span class="deadline-label">${label}${expired ? ' · 已截止' : ''}</span><span class="deadline-local">${localized(value)}</span><span class="deadline-original">${escape(detail)}</span></div>`;
  }
  function deadlineGrid(cycle, now) {
    return `<div class="deadline-grid">${timeCell(cycle.abstract, 'Abstract / 摘要', now, cycle.abstract_note)}${timeCell(cycle.paper, 'Full paper / 全文', now)}</div>`;
  }
  function countdown(value, now) {
    const b = bounds(value);
    if (!b.exact) {
      const days = Math.max(0, Math.round((b.start - now) / DAY));
      return days <= 1 ? '临近截止日（日期级）' : `约 ${days} 天（日期级）`;
    }
    const minutes = Math.max(0, Math.floor((b.end - now) / 60000));
    if (minutes < 1) return '不足 1 分钟';
    return `${Math.floor(minutes / 1440)} 天 ${Math.floor(minutes / 60) % 24} 时 ${minutes % 60} 分`;
  }
  function renderCard(conf, s, now, opened) {
    const badge = s.status === 'upcoming' ? (s.uncertainTime ? '截止时刻待核验' : s.registeredOnly ? '仅限已交摘要' : '仍有投稿窗口') : (s.status === 'pending' ? '日期待公布' : '本届已截止');
    const clock = s.next && !s.uncertainTime ? `<span class="countdown">${countdown(s.next, now)}<small>至${s.nextLabel}</small></span>` : '';
    const current = s.cycle ? `<p class="next-cycle">${escape(s.cycle.label)}</p>${deadlineGrid(s.cycle, now)}` : '';
    const warning = (s.registeredOnly ? '<p class="registration-note">本轮摘要已截止：只有已按要求提交摘要的论文才能继续。其他轮次见下方。</p>' : '') + (s.uncertainTime ? '<p class="registration-note">官方时间/时区尚未核验，不能据此判断目前仍可投稿。请打开官方入口确认。</p>' : '');
    const cycles = conf.cycles.length ? `<details class="cycle-details" data-cycle-id="${escape(conf.id)}"${opened.has(conf.id) ? ' open' : ''}><summary>全部已记录轮次 / 历史日期（${conf.cycles.length}）</summary>${conf.cycles.map(c => `<div class="cycle-item"><p class="cycle-title">${escape(c.label)}</p>${deadlineGrid(c, now)}</div>`).join('')}</details>` : '';
    return `<article class="conference" data-status="${s.status}" id="${escape(conf.id)}"><div class="conference-top"><div><h2>${escape(conf.name)}<span class="edition">${conf.edition}</span></h2><p class="full-name">${escape(conf.full_name)}</p><p class="track-line">${escape(data.areas[conf.area])} · ${escape(conf.track)}</p></div><div class="conference-status"><span class="badge ${s.registeredOnly ? 'registered' : s.status}">${badge}</span>${clock}</div></div>${current}${warning}<p class="conference-note">${escape(conf.note)}</p><div class="source-row">${conf.sources.map(source => `<a href="${escape(source.url)}" target="_blank" rel="noopener noreferrer">${escape(source.label)} ↗</a>`).join('')}<span class="checked">核对 ${escape(conf.checked)}</span></div>${cycles}</article>`;
  }
  function draw() {
    const now = Date.now();
    const query = search.value.trim().toLowerCase();
    const focused = document.activeElement;
    const focusCard = list.contains(focused) ? focused.closest('.conference')?.id : null;
    const focusTag = focused.tagName;
    const focusHref = focused.getAttribute('href');
    const opened = new Set([...list.querySelectorAll('details[open]')].map(el => el.dataset.cycleId));
    const items = data.conferences.map(conf => ({conf, s: state(conf, now)}));
    const counts = {upcoming:0, pending:0, closed:0};
    items.forEach(({s}) => counts[s.status]++);
    document.getElementById('live-counts').textContent = `${counts.upcoming} 个仍有窗口 · ${counts.pending} 个日期待公布 · ${counts.closed} 个本届已截止`;
    document.getElementById('today').textContent = '今天 ' + new Intl.DateTimeFormat('sv-SE', {timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(now)) + '（北京）';
    const selected = items.filter(({conf, s}) => (area === 'all' || conf.area === area)
      && (status.value === 'all' || status.value === s.status)
      && `${conf.name} ${conf.full_name} ${conf.edition}`.toLowerCase().includes(query));
    const rank = {upcoming:0, pending:1, closed:2};
    selected.sort((a,b) => rank[a.s.status] - rank[b.s.status] || a.s.sort - b.s.sort || a.conf.name.localeCompare(b.conf.name));
    list.innerHTML = selected.map(({conf,s}) => renderCard(conf, s, now, opened)).join('');
    document.getElementById('results-label').textContent = `显示 ${selected.length} / ${data.conferences.length} 个会议 · 按下一截止节点排序`;
    document.getElementById('empty-state').hidden = selected.length > 0;
    if (focusCard) {
      const card = document.getElementById(focusCard);
      const target = focusTag === 'SUMMARY' ? card?.querySelector('summary')
        : [...(card?.querySelectorAll('a') || [])].find(a => a.getAttribute('href') === focusHref);
      target?.focus({preventScroll: true});
    }
  }
  document.getElementById('area-filters').addEventListener('click', event => {
    const button = event.target.closest('button[data-area]');
    if (!button) return;
    area = button.dataset.area;
    document.querySelectorAll('[data-area]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    draw();
  });
  search.addEventListener('input', draw);
  status.addEventListener('change', draw);
  timezone.addEventListener('change', draw);
  document.getElementById('reset').addEventListener('click', () => {
    area = 'all'; search.value = ''; status.value = 'all'; timezone.value = 'Asia/Shanghai';
    document.querySelectorAll('[data-area]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.area === 'all')));
    draw();
  });
  draw();
  // Rebuild with open details and focus preserved, even across a deadline.
  setInterval(draw, 60000);
})();
