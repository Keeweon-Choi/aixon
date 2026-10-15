(() => {
  const token = new URLSearchParams(location.search).get('token') || '';
  const storageKey = 'aixon-review-decisions';
  const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
  let records = [],
    selected = 0,
    approvedSinceCommit = 0,
    defaultBy = '',
    agentSession = false;
  const $ = (s) => document.querySelector(s);
  const api = (path, options = {}) =>
    fetch(`${path}?token=${encodeURIComponent(token)}`, options).then(async (r) => {
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || r.statusText);
      return body;
    });
  const esc = (value) =>
    String(value ?? '').replace(
      /[&<>"']/g,
      (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch],
    );
  // Only http(s) URLs become links; anything else (javascript:, data:) is shown as text.
  const link = (url, label) =>
    /^https?:\/\//i.test(String(url || ''))
      ? `<a href="${esc(url)}" target="_blank" rel="noreferrer">${esc(label)}</a>`
      : esc(url || '—');
  const text = (value) =>
    value === undefined || value === null || value === ''
      ? '—'
      : Array.isArray(value)
        ? value.map(esc).join(', ')
        : typeof value === 'object'
          ? esc(JSON.stringify(value))
          : esc(value);
  function visible() {
    const q = $('#search').value.toLowerCase();
    return records.filter(
      (r) =>
        (!$('#state').value || r.state === $('#state').value) &&
        (!$('#kind').value || r.kind === $('#kind').value) &&
        (!$('#pre').value || r.pre_review?.recommendation === $('#pre').value) &&
        (!q || `${r.id} ${r.title}`.toLowerCase().includes(q)) &&
        crossMatches(r),
    );
  }
  function crossMatches(r) {
    const wanted = $('#cross').value;
    if (!wanted) return true;
    const reviews = r.cross_review || [];
    if (wanted === 'none') return !reviews.length;
    const failures = reviews.some(
      (x) =>
        x.decision !== 'approve' ||
        (x.unchecked || []).length ||
        (x.checks || []).some(
          (c) =>
            !['supported', 'computed', 'analogy-sourced', 'no-claim'].includes(c.verdict) ||
            (c.sources || []).some((s) => s.confirm && s.confirm !== 'found'),
        ),
    );
    return wanted === 'fail' ? failures : reviews.length > 0 && !failures;
  }
  function renderQueue() {
    const items = visible();
    if (!items.includes(records[selected])) selected = records.indexOf(items[0]);
    $('#counts').textContent =
      `${items.length} / ${records.length}건 · 결정 ${Object.keys(saved).length}건`;
    $('#queue').innerHTML = items
      .map(
        (r) =>
          `<li><button data-id="${esc(r.id)}" ${records[selected] === r ? 'aria-current="true"' : ''}><strong>${esc(r.title)}</strong><div class="row-meta"><span>${esc(r.type_label)}</span><span class="chip state-${esc(r.state)}">${esc(r.state)}</span>${r.public ? '<span class="chip">공개</span>' : ''}${r.pre_review ? `<span class="chip">사전:${esc(r.pre_review.recommendation)}</span>` : ''}</div></button></li>`,
      )
      .join('');
    $('#queue')
      .querySelectorAll('button')
      .forEach(
        (b) =>
          (b.onclick = () => {
            selected = records.findIndex((r) => r.id === b.dataset.id);
            render();
          }),
      );
  }
  const field = (name, value) => `<dt>${esc(name)}</dt><dd>${text(value)}</dd>`;
  function evidence(items) {
    return (items || [])
      .map(
        (e) =>
          `<article class="card"><strong>${esc(e.source_title)} ${e.source_version ? `(${esc(e.source_version)})` : ''}</strong><div>${esc(e.type)} · ${esc(e.stance)} · ${esc(e.locator || '위치 미지정')}</div><blockquote lang="en">${esc(e.quote || '')}</blockquote>${e.text_link ? link(e.text_link, '원문 열기') : ''}</article>`,
      )
      .join('');
  }
  function details(r) {
    const d = r.details;
    if (r.kind === 'claim')
      return `<dl>${field('술어', `${d.predicate_label || d.predicate} (${d.predicate})`)}${field('주어', d.subject)}${field('목적어', d.object)}${field('상태', d.status)}${field('신뢰도', d.confidence)}${field('한정어', d.qualifiers)}${field('메모', d.note)}</dl><h2>근거</h2>${evidence(d.evidence) || '<p>근거 없음</p>'}`;
    if (r.kind === 'wiki')
      return `<dl>${field('상태', d.status)}${field('대상 엔티티', d.entity)}${field('인용 Claim', d.claims)}</dl><h2>MDX 원문</h2><pre>${esc(d.source)}</pre>`;
    if (r.kind === 'item')
      return `<dl>${field('문제', d.prompt)}${field('선택지', d.choices)}${field('정답', d.answer)}${field('허용 오차', d.tolerance)}${field('해설', d.rationale)}</dl>`;
    let output = `<dl>${field('별칭', d.aliases)}${field('요약', d.summary)}${field('분야', d.fields)}</dl>`;
    if (d.paper)
      output += `<h2>논문 메타데이터</h2><dl>${field('제목', d.paper.title)}${field('저자', d.paper.authors)}${field('날짜', d.paper.date)}${field('학회', d.paper.venue)}<dt>arXiv</dt><dd>${link(d.paper.arxiv, d.paper.arxiv)}</dd></dl>`;
    return output;
  }
  function cross(r) {
    if (!(r.cross_review || []).length)
      return '<section class="cross"><h2>교차 검증</h2><p>교차 검증 보고서가 없습니다.</p></section>';
    const blocks = r.cross_review
      .map((x) => {
        const problems = r.cross_review_problems?.[x.release] || [];
        const rows = (x.checks || [])
          .map((c) => {
            const bad =
              !['supported', 'computed', 'analogy-sourced', 'no-claim'].includes(c.verdict) ||
              (c.sources || []).some((s) => s.confirm && s.confirm !== 'found');
            return `<tr class="${bad ? 'fail' : ''}"><td>${esc(c.field)}</td><td>${esc(c.verdict)}</td><td>${(c.sources || []).map((s) => `${link(s.url, '원문')} (${esc(s.tier || '—')})`).join('<br>')}</td><td>${(c.sources || []).map((s) => esc(s.passage || '—')).join('<br>')}</td><td>${(c.sources || []).map((s) => esc(s.confirm || '미확인')).join('<br>')}</td></tr>`;
          })
          .join('');
        return `<article class="card ${x.decision === 'approve' && !problems.length ? 'ok' : 'bad'}"><h3>${esc(x.reviewer)} · ${esc(x.decision)} · ${esc(x.start)}</h3><p>수정: ${esc(x.fix || '없음')}<br>미확인: ${text(x.unchecked)}</p><table><thead><tr><th>필드</th><th>판정</th><th>출처 / 등급</th><th>구절</th><th>대조</th></tr></thead><tbody>${rows}</tbody></table>${problems.length ? `<pre>${esc(problems.join('\n'))}</pre>` : ''}</article>`;
      })
      .join('');
    return `<section class="cross"><h2>교차 검증</h2>${blocks}</section>`;
  }
  function renderDetail() {
    const r = records[selected];
    if (!r) return;
    const pending = saved[r.id] || {};
    $('#detail').innerHTML =
      `<div class="hero"><div><h2>${esc(r.title)}</h2><p>${esc(r.id)} · ${esc(r.type_label)}</p></div><div><span class="chip state-${esc(r.state)}">${esc(r.state)}</span> ${r.public ? '<span class="chip">공개</span>' : ''}<br>${r.approved_by ? `승인자: ${esc(r.approved_by)}` : ''}</div></div>${details(r)}${r.pre_review ? `<section class="pre"><h2>사전 검수: ${esc(r.pre_review.recommendation)}</h2><p>${esc(r.pre_review.notes)}</p>${r.pre_review.fix ? `<pre>${esc(r.pre_review.fix)}</pre>` : ''}<small>${esc(r.pre_review.worksheet)}</small></section>` : ''}${cross(r)}<section class="decision"><h2>결정</h2><div class="actions"><button data-decision="approve" class="${pending.decision === 'approve' ? 'selected' : ''}">승인 (a)</button><button data-decision="fix" class="${pending.decision === 'fix' ? 'selected' : ''}">수정 필요 (f)</button><button data-decision="exclude" class="${pending.decision === 'exclude' ? 'selected' : ''}">제외 (x)</button></div><label>메모 <textarea id="note" rows="3">${esc(pending.note || '')}</textarea></label><label class="publish ${r.kind === 'wiki' ? 'visible' : ''}"><input id="publish" type="checkbox" ${pending.publish ? 'checked' : ''} /> 승인 후 게시</label></section>`;
    $('#detail')
      .querySelectorAll('[data-decision]')
      .forEach((b) => (b.onclick = () => choose(b.dataset.decision)));
  }
  function choose(decision) {
    const r = records[selected];
    if (!r) return;
    saved[r.id] = {
      decision,
      note: $('#note')?.value || '',
      publish: $('#publish')?.checked || false,
    };
    localStorage.setItem(storageKey, JSON.stringify(saved));
    render();
  }
  function render() {
    renderQueue();
    renderDetail();
  }
  async function save() {
    const current = records[selected];
    // Only keep the note of a record that already has a decision; an undecided entry would make
    // the server refuse the whole batch.
    if (current && $('#note') && saved[current.id]) {
      saved[current.id] = {
        ...(saved[current.id] || {}),
        note: $('#note').value,
        publish: $('#publish')?.checked || false,
      };
    }
    const by = $('#reviewer').value.trim();
    localStorage.setItem('aixon-reviewer', by);
    try {
      const result = await api('/api/decisions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          by,
          decisions: Object.entries(saved).map(([id, v]) => ({ id, ...v })),
        }),
      });
      approvedSinceCommit += result.approved.length;
      localStorage.removeItem(storageKey);
      Object.keys(saved).forEach((k) => delete saved[k]);
      $('#message').textContent =
        `기록 완료: 승인 ${result.approved.length}, 게시 ${result.published.length}, 건너뜀 ${result.skipped.length}, 실패 ${result.failed.length}\n${result.decision_file}`;
      await load();
    } catch (e) {
      $('#message').textContent = `기록 거부/실패: ${e.message}`;
    }
  }
  async function commit() {
    try {
      const output = await api('/api/commit-push', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ by: $('#reviewer').value.trim(), approved: approvedSinceCommit }),
      });
      approvedSinceCommit = 0;
      $('#message').textContent = output.output;
    } catch (e) {
      $('#message').textContent = `커밋/배포 거부 또는 실패: ${e.message}`;
    }
  }
  async function load() {
    try {
      const data = await api('/api/queue');
      records = data.records;
      defaultBy = data.default_by;
      agentSession = data.agent_session;
      $('#reviewer').value = localStorage.getItem('aixon-reviewer') || defaultBy;
      render();
    } catch (e) {
      $('#detail').innerHTML = `<p class="bad">대기열을 열 수 없습니다: ${esc(e.message)}</p>`;
    }
  }
  document.addEventListener('DOMContentLoaded', () => {
    document.body.insertAdjacentHTML(
      'beforeend',
      '<footer id="footer-actions"><button id="save">결정 기록</button><button id="commit">커밋하고 배포</button><output id="message"></output></footer>',
    );
    ['search', 'state', 'kind', 'pre', 'cross'].forEach((id) =>
      $(`#${id}`).addEventListener('input', render),
    );
    $('#save').onclick = save;
    $('#commit').onclick = commit;
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return; // Ctrl+A / Ctrl+F are not decisions
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
      const items = visible();
      const at = items.indexOf(records[selected]);
      if (e.key === 'j' && at < items.length - 1) {
        selected = records.indexOf(items[at + 1]);
        render();
      }
      if (e.key === 'k' && at > 0) {
        selected = records.indexOf(items[at - 1]);
        render();
      }
      if ({ a: 'approve', f: 'fix', x: 'exclude' }[e.key])
        choose({ a: 'approve', f: 'fix', x: 'exclude' }[e.key]);
    });
    load();
  });
})();
