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
      navigator.share({ title: 'Track Her Case', text: a.dataset.shareText.replace(/\s*Give or share: \S+$/, ''), url: a.dataset.shareUrl })
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
})();
