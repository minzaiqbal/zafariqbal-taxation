(function () {
  var b = document.querySelector('.menu-btn'), n = document.getElementById('nav');
  if (b && n) {
    b.addEventListener('click', function () {
      var o = n.classList.toggle('open');
      b.setAttribute('aria-expanded', o);
    });
  }
  var g = document.getElementById('gate'), ok = document.getElementById('gate-accept');
  if (g && ok) {
    var seen = false;
    try { seen = localStorage.getItem('bci_ack') === '1'; } catch (e) {}
    if (!seen) { g.hidden = false; document.body.style.overflow = 'hidden'; ok.focus(); }
    ok.addEventListener('click', function () {
      try { localStorage.setItem('bci_ack', '1'); } catch (e) {}
      g.hidden = true; document.body.style.overflow = '';
    });
  }
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });
})();
