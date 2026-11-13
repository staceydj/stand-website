/* Track Her Case campaign page */
(() => {
  /* One-tap copy for bank details and the page link */
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    const label = btn.textContent;
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
        btn.textContent = 'Copied';
        btn.classList.add('is-done');
      } catch (err) {
        btn.textContent = 'Press and hold to copy';
      }
      setTimeout(() => { btn.textContent = label; btn.classList.remove('is-done'); }, 2000);
    });
  });

  /* The dock's Share button opens the phone's share sheet where there is one
     (WhatsApp, Instagram, Messages, email...). Elsewhere it opens WhatsApp. */
  document.querySelectorAll('[data-share]').forEach((a) => {
    if (!navigator.share) return;
    a.addEventListener('click', (ev) => {
      ev.preventDefault();
      navigator.share({ title: 'Track Her Case', text: a.dataset.shareText.replace(/\s*Watch the 90-second film and give: \S+$/, ''), url: a.dataset.shareUrl })
        .catch(() => {});
    });
  });

  /* Tuck the dock away while the hero buttons, the giving options or the footer are on screen */
  const dock = document.querySelector('.dock');
  const watch = [document.querySelector('.cta-row'), document.getElementById('give'), document.querySelector('.foot')].filter(Boolean);
  if (dock && 'IntersectionObserver' in window) {
    const seen = new Set();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => (en.isIntersecting ? seen.add(en.target) : seen.delete(en.target)));
      dock.classList.toggle('is-hidden', seen.size > 0);
    }, { threshold: 0.25 });
    watch.forEach((el) => io.observe(el));
  }

  /* ---------- Currency switch and the two giving doors ---------- */
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } } };
  const tz = (() => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { return ''; } })();
  const inSA = /^Africa\/(Johannesburg|Maseru|Mbabane|Gaborone|Windhoek)/.test(tz);
  const guess = inSA ? 'ZAR' : tz === 'Europe/London' ? 'GBP' : tz.startsWith('Europe/') ? 'EUR' : 'USD';

  const setCur = (c) => {
    document.querySelectorAll('.cur-switch button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.cur === c)));
    document.querySelectorAll('.ladder').forEach((l) => { l.hidden = l.dataset.cur !== c; });
  };
  const tabs = [...document.querySelectorAll('.doors [role="tab"]')];
  const setDoor = (d) => {
    tabs.forEach((t) => {
      const on = t.id === 'tab-' + d;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  };
  document.querySelectorAll('.cur-switch button').forEach((b) => b.addEventListener('click', () => {
    setCur(b.dataset.cur); store.set('thc-cur', b.dataset.cur);
    setDoor(b.dataset.cur === 'ZAR' ? 'sa' : 'abroad');
  }));
  tabs.forEach((t) => {
    t.addEventListener('click', () => setDoor(t.id.slice(4)));
    t.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const next = tabs[(tabs.indexOf(t) + 1) % tabs.length]; setDoor(next.id.slice(4)); next.focus();
    });
  });
  document.querySelectorAll('[data-door]').forEach((a) => a.addEventListener('click', () => setDoor(a.dataset.door)));
  const cur = store.get('thc-cur') || guess;
  setCur(cur);
  setDoor(cur === 'ZAR' ? 'sa' : 'abroad');

  /* ---------- Progress towards R150,000 (the number lives in progress.txt) ---------- */
  const prog = document.querySelector('.progress');
  if (prog && window.fetch) {
    fetch('progress.txt', { cache: 'no-store' }).then((r) => (r.ok ? r.text() : '')).then((txt) => {
      const raised = parseInt(String(txt).replace(/[^0-9]/g, ''), 10);
      if (Number.isNaN(raised)) return;
      const goal = +prog.dataset.goal;
      const line = prog.querySelector('.progress-line');
      if (raised <= 0) {
        line.innerHTML = '<b>R150,000</b> to keep it running through the festive season. Be one of the first to give.';
      } else {
        prog.querySelector('[data-raised]').textContent = 'R' + String(raised).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      }
      const bar = prog.querySelector('.bar');
      bar.setAttribute('aria-valuenow', String(raised));
      prog.hidden = false;
      requestAnimationFrame(() => { bar.firstElementChild.style.width = Math.min(100, (raised / goal) * 100) + '%'; });
    }).catch(() => {});
  }
})();
