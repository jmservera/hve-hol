/* HyperVelocity Engineering · hands-on workshop guide
   Small progressive enhancements: mobile navigation, editable templates saved in this browser,
   Copy as Markdown, copy buttons for code, hand-in check boxes and the resources filter.
   Everything stays in the browser (localStorage); nothing is sent anywhere. */
(function () {
  'use strict';

  var doc = document;
  var page = doc.body.getAttribute('data-page') || 'page';
  var PREFIX = 'hve-guide:v1:';

  var store = (function () {
    try {
      var k = PREFIX + 'probe';
      window.localStorage.setItem(k, '1');
      window.localStorage.removeItem(k);
      return window.localStorage;
    } catch (e) {
      return null;
    }
  })();

  function getItem(key) {
    if (!store) return null;
    try { return store.getItem(key); } catch (e) { return null; }
  }
  function setItem(key, value) {
    if (!store) return;
    try {
      if (value === null) store.removeItem(key); else store.setItem(key, value);
    } catch (e) { /* storage full or blocked: ignore */ }
  }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  /* ---------------------------------------------------------------- mobile navigation */
  var toggle = doc.querySelector('.nav-toggle');
  var sidebar = doc.getElementById('sidebar');
  var scrim = doc.querySelector('.scrim');

  function setNav(open) {
    doc.body.classList.toggle('nav-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (scrim) scrim.hidden = !open;
    if (open && sidebar) {
      var first = sidebar.querySelector('[aria-current="page"]') || sidebar.querySelector('a');
      if (first) first.focus();
    }
  }
  if (toggle && sidebar) {
    toggle.addEventListener('click', function () { setNav(!doc.body.classList.contains('nav-open')); });
    if (scrim) scrim.addEventListener('click', function () { setNav(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && doc.body.classList.contains('nav-open')) { setNav(false); toggle.focus(); }
    });
    each(sidebar.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () { setNav(false); });
    });
    var current = sidebar.querySelector('[aria-current="page"]');
    if (current) {
      var top = current.offsetTop - sidebar.clientHeight / 2;
      if (top > 0) sidebar.scrollTop = top;
    }
  }

  /* ---------------------------------------------------------------- clipboard */
  function flash(btn, text) {
    var original = btn.getAttribute('data-label') || btn.textContent;
    btn.setAttribute('data-label', original);
    btn.textContent = text;
    btn.classList.add('is-done');
    window.setTimeout(function () {
      btn.textContent = original;
      btn.classList.remove('is-done');
    }, 1600);
  }
  function copyText(text, btn) {
    function fallback() {
      var ta = doc.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      doc.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = doc.execCommand('copy'); } catch (e) { ok = false; }
      doc.body.removeChild(ta);
      flash(btn, ok ? 'Copied' : 'Copy failed');
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { flash(btn, 'Copied'); }, fallback);
    } else {
      fallback();
    }
  }

  /* ---------------------------------------------------------------- Markdown export */
  function textOf(el) {
    return (el.innerText || el.textContent || '').replace(/\u00a0/g, ' ').replace(/\s+$/g, '').replace(/^\s+/g, '');
  }
  function mdCell(el) {
    return textOf(el).replace(/\|/g, '\\|').replace(/\r?\n+/g, '<br>') || ' ';
  }
  function tableToMarkdown(table, title) {
    var lines = ['### ' + title, ''];
    each(table.rows, function (row, i) {
      var cells = Array.prototype.map.call(row.cells, mdCell);
      lines.push('| ' + cells.join(' | ') + ' |');
      if (i === 0) lines.push('|' + cells.map(function () { return ' --- '; }).join('|') + '|');
    });
    return lines.join('\n') + '\n';
  }
  function canvasToMarkdown(tpl, title) {
    var lines = ['### ' + title, ''];
    each(tpl.querySelectorAll('.canvas-cell'), function (cell) {
      var heading = cell.getAttribute('data-md') || textOf(cell.querySelector('.canvas-title'));
      var body = textOf(cell.querySelector('.canvas-fill'));
      lines.push('**' + heading + '**', '', body || '…', '');
    });
    return lines.join('\n');
  }

  /* ---------------------------------------------------------------- editable templates */
  each(doc.querySelectorAll('[data-tpl]'), function (tpl) {
    var id = tpl.getAttribute('data-tpl');
    var key = PREFIX + (tpl.getAttribute('data-store') || page + ':' + id);
    var cells = tpl.querySelectorAll('[contenteditable="true"]');
    var heading = tpl.querySelector('.tpl-head h3');
    var title = heading ? heading.textContent.replace(/\s+/g, ' ').trim() : 'Template';
    var timer = null;

    try {
      var saved = JSON.parse(getItem(key) || 'null');
      if (saved && saved.length === cells.length) {
        each(cells, function (c, i) { if (saved[i]) c.innerText = saved[i]; });
      }
    } catch (e) { /* ignore corrupt data */ }

    function save() {
      var values = Array.prototype.map.call(cells, textOf);
      var any = values.some(function (v) { return v.length > 0; });
      setItem(key, any ? JSON.stringify(values) : null);
    }

    each(cells, function (c) {
      c.addEventListener('input', function () {
        if (!c.textContent.replace(/\u00a0/g, ' ').trim() && !c.querySelector('img')) c.innerHTML = '';
        window.clearTimeout(timer);
        timer = window.setTimeout(save, 250);
      });
      c.addEventListener('blur', save);
      c.addEventListener('paste', function (e) {
        var data = e.clipboardData || window.clipboardData;
        if (!data) return;
        e.preventDefault();
        var text = data.getData('text') || '';
        if (!doc.execCommand || !doc.execCommand('insertText', false, text)) {
          c.innerText += text;
        }
      });
    });

    var copyBtn = tpl.querySelector('[data-action="copy-md"]');
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var md = tpl.getAttribute('data-kind') === 'canvas'
          ? canvasToMarkdown(tpl, title)
          : tableToMarkdown(tpl.querySelector('table'), title);
        copyText(md, copyBtn);
      });
    }
    var clearBtn = tpl.querySelector('[data-action="clear"]');
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        var hasText = Array.prototype.some.call(cells, function (c) { return textOf(c).length > 0; });
        if (!hasText) { flash(clearBtn, 'Empty'); return; }
        if (!window.confirm('Clear everything typed in "' + title + '"?')) return;
        each(cells, function (c) { c.innerHTML = ''; });
        setItem(key, null);
        flash(clearBtn, 'Cleared');
      });
    }
  });

  /* ---------------------------------------------------------------- hand-in check boxes */
  each(doc.querySelectorAll('input[type="checkbox"][data-key]'), function (cb) {
    var key = PREFIX + page + ':check:' + cb.getAttribute('data-key');
    if (getItem(key) === '1') cb.checked = true;
    cb.addEventListener('change', function () { setItem(key, cb.checked ? '1' : null); });
  });

  /* ---------------------------------------------------------------- code copy buttons */
  each(doc.querySelectorAll('[data-copy-code]'), function (btn) {
    btn.addEventListener('click', function () {
      var pre = doc.getElementById(btn.getAttribute('data-copy-code'));
      if (pre) copyText(pre.textContent.replace(/\s+$/, '') + '\n', btn);
    });
  });

  /* ---------------------------------------------------------------- resources filter */
  var filter = doc.getElementById('res-filter');
  if (filter) {
    var count = doc.getElementById('res-count');
    filter.addEventListener('input', function () {
      var q = filter.value.trim().toLowerCase();
      each(doc.querySelectorAll('[data-res-item]'), function (item) {
        item.hidden = q.length > 0 && item.textContent.toLowerCase().indexOf(q) === -1;
      });
      each(doc.querySelectorAll('[data-res-group]'), function (group) {
        group.hidden = q.length > 0 && !group.querySelector('[data-res-item]:not([hidden])');
      });
      each(doc.querySelectorAll('[data-res-section]'), function (section) {
        section.hidden = q.length > 0 && !section.querySelector('[data-res-item]:not([hidden])');
      });
      if (count) {
        var n = doc.querySelectorAll('[data-res-item]:not([hidden])').length;
        count.textContent = q ? n + (n === 1 ? ' match' : ' matches') : '';
      }
    });
  }
})();
