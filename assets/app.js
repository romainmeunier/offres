document.addEventListener('DOMContentLoaded', () => {
  const q = document.querySelector('#q');
  if (q) {
    q.addEventListener('input', () => {
      const v = q.value.toLowerCase();
      document.querySelectorAll('[data-card]').forEach(c => {
        const text = c.dataset.card.toLowerCase();
        c.style.display = text.includes(v) ? '' : 'none';
      });
    });
  }
  document.querySelectorAll('[data-lang]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const lang = btn.dataset.lang;
      document.querySelectorAll('[data-lang]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('[data-locale]').forEach(s => {
        s.style.display = s.dataset.locale === lang ? '' : 'none';
      });
    });
  });
});
