(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Nav: scrolled state, mobile menu, dropdowns ---------- */
  const nav = document.getElementById('nav');
  const burger = document.getElementById('burger');
  const toTop = document.getElementById('to-top');

  const onScroll = () => {
    const y = window.scrollY;
    nav.classList.toggle('is-scrolled', y > 40);
    toTop.classList.toggle('is-visible', y > window.innerHeight);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const setMenu = (open) => {
    nav.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('menu-open')));
  nav.querySelectorAll('.nav-menu a').forEach((a) => a.addEventListener('click', () => setMenu(false)));

  const items = [...nav.querySelectorAll('.nav-item')];
  const closeAll = (except) => items.forEach((it) => {
    if (it === except) return;
    it.classList.remove('is-open');
    it.querySelector('.nav-toggle').setAttribute('aria-expanded', 'false');
  });
  items.forEach((it) => {
    const btn = it.querySelector('.nav-toggle');
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = !it.classList.contains('is-open');
      closeAll(it);
      it.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('.nav-item')) closeAll(); });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    closeAll();
    if (nav.classList.contains('menu-open')) { setMenu(false); burger.focus(); }
  });

  /* Footer dropdowns: only one open at a time */
  const footerDetails = [...document.querySelectorAll('.footer-nav details')];
  footerDetails.forEach((d) => d.addEventListener('toggle', () => {
    if (d.open) footerDetails.forEach((o) => { if (o !== d) o.open = false; });
  }));

  /* ---------- Reveal on scroll ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }

  /* ---------- Parallax layers (hero + about) ---------- */
  const layers = [...document.querySelectorAll('[data-depth]')];
  if (layers.length && !reduceMotion) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const vh = window.innerHeight;
      layers.forEach((img) => {
        // Layers sit at rest until their section starts scrolling away, then drift down
        // at a fraction of scroll speed (deeper layers drift more, so they feel farther away).
        const host = img.closest('section').getBoundingClientRect();
        if (host.bottom < 0 || host.top > vh) return;
        const depth = parseFloat(img.dataset.depth);
        const offset = Math.max(0, -host.top) * depth;
        img.style.setProperty('--py', `${offset.toFixed(1)}px`);
      });
    };
    const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    update();
  }

  /* ---------- Testimonial slider ---------- */
  const slider = document.getElementById('slider');
  if (slider) {
    const slides = [...slider.querySelectorAll('.slide')];
    const dotsWrap = slider.querySelector('.slider-dots');
    let index = 0;
    let timer;
    const dots = slides.map((_, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', `Show testimonial ${i + 1}`);
      b.addEventListener('click', () => { go(i); restart(); });
      dotsWrap.appendChild(b);
      return b;
    });
    const go = (i) => {
      index = (i + slides.length) % slides.length;
      slides.forEach((s, n) => {
        s.classList.toggle('is-active', n === index);
        s.setAttribute('aria-hidden', String(n !== index));
      });
      dots.forEach((d, n) => d.setAttribute('aria-current', String(n === index)));
    };
    const restart = () => {
      clearInterval(timer);
      if (!reduceMotion) timer = setInterval(() => go(index + 1), 7000);
    };
    slider.querySelector('.prev').addEventListener('click', () => { go(index - 1); restart(); });
    slider.querySelector('.next').addEventListener('click', () => { go(index + 1); restart(); });
    slider.addEventListener('mouseenter', () => clearInterval(timer));
    slider.addEventListener('mouseleave', restart);
    slider.addEventListener('focusin', () => clearInterval(timer));
    let startX = null;
    slider.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener('touchend', (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) { go(index + (dx < 0 ? 1 : -1)); restart(); }
      startX = null;
    });
    go(0);
    restart();
  }

  /* ---------- Contact form: compose an e-mail ---------- */
  const form = document.getElementById('contact-form');
  if (form) {
    const status = form.querySelector('.form-status');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const missing = ['name', 'email', 'message'].filter((k) => !String(data.get(k) || '').trim());
      const email = String(data.get('email') || '');
      if (missing.length || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        status.textContent = 'Please fill in your name, a valid e-mail address and a message.';
        const first = form.querySelector(`[name="${missing[0] || 'email'}"]`);
        if (first) first.focus();
        return;
      }
      const body = [
        String(data.get('message')),
        '',
        `Name: ${data.get('name')}`,
        data.get('company') ? `Company: ${data.get('company')}` : '',
        `E-Mail: ${email}`,
        data.get('phone') ? `Phone: ${data.get('phone')}` : '',
      ].filter((l, i) => i < 2 || l).join('\n');
      const subject = `Inquiry via website from ${data.get('name')}`;
      window.location.href = `mailto:stacey@standaction.co.za?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      status.textContent = 'Thank you very much. Your e-mail program should now open with your message.';
    });
  }
  /* ---------- Copy buttons (bank details) ---------- */
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy);
        btn.textContent = 'Copied';
      } catch (err) {
        btn.textContent = 'Select to copy';
      }
      setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
    });
  });
  /* ---------- WhatsApp share (appeal page) ---------- */
  document.querySelectorAll('[data-share-wa]').forEach((a) => {
    const msg = 'STAND works where justice, health, protection and implementation meet, so support reaches the people too often failed by the systems meant to serve them. Support the work and share: ' + window.location.href.split('#')[0];
    a.href = 'https://wa.me/?text=' + encodeURIComponent(msg);
  });
})();
