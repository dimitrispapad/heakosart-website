/* TheakosArt — motion system (no dependencies) */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- door: intro + page transitions ---------- */
  function openDoor() { doc.classList.remove('is-intro'); doc.classList.add('is-open'); }
  var seen = false;
  try { seen = sessionStorage.getItem('ta-seen') === '1'; sessionStorage.setItem('ta-seen', '1'); } catch (e) {}
  if (reduce) { doc.classList.add('is-open'); }
  else if (!seen) { doc.classList.add('is-intro'); setTimeout(openDoor, 1900); }
  else { requestAnimationFrame(function () { setTimeout(openDoor, 80); }); }
  window.addEventListener('pageshow', function (e) { if (e.persisted) openDoor(); });

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || reduce) return;
    var href = a.getAttribute('href');
    if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank' || a.hasAttribute('download')) return;
    if (/^(#|mailto:|tel:|https?:)/.test(href)) return;
    e.preventDefault();
    doc.classList.remove('is-open');
    setTimeout(function () { window.location.href = a.href; }, 850);
  });

  /* ---------- header + menu ---------- */
  var hdr = $('.hdr'), menu = $('.menu'), burger = $('.burger'), lastY = 0;
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open);
      burger.textContent = open ? burger.dataset.close : burger.dataset.open;
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  /* ---------- split headings into words ---------- */
  $$('[data-split]').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words.map(function (w, i) {
      return '<span class="w" aria-hidden="true"><span style="transition-delay:' + (i * 55) + 'ms">' + w + '</span></span>';
    }).join(' ');
  });

  /* ---------- reveal on scroll ---------- */
  /* An element clipped to zero width never "intersects", so apertures are watched through their parent. */
  var targets = $$('[data-aperture],[data-split],[data-fade],[data-rule]');
  if ('IntersectionObserver' in window && !reduce) {
    var watch = new Map();
    targets.forEach(function (t) {
      var w = t.hasAttribute('data-aperture') ? t.parentElement : t;
      if (!watch.has(w)) watch.set(w, []);
      watch.get(w).push(t);
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        watch.get(en.target).forEach(function (t) { t.classList.add('in'); });
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    setTimeout(function () { watch.forEach(function (v, w) { io.observe(w); }); }, seen ? 450 : 2100);
  } else { targets.forEach(function (t) { t.classList.add('in'); }); }

  /* ---------- counters ---------- */
  $$('[data-count]').forEach(function (el) {
    var end = parseInt(el.dataset.count, 10), suffix = el.dataset.suffix || '';
    if (reduce || !('IntersectionObserver' in window)) { el.textContent = end + suffix; return; }
    el.textContent = '0' + suffix;
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting) return; o.disconnect();
      var t0 = performance.now(), dur = end > 1000 ? 1 : 1600;
      (function tick(t) {
        var p = clamp((t - t0) / dur, 0, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 4))) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }, { threshold: .6 }).observe(el);
  });

  /* ---------- hero slideshow ---------- */
  var hero = $('[data-hero]');
  if (hero) {
    var slides = $$('.hero__slide', hero), cap = $('.hero__cap', hero), cnt = $('.hero__count', hero), bar = $('.hero__bar', hero);
    var idx = 0, timer;
    var show = function (n) {
      slides.forEach(function (s) { s.classList.remove('is-prev'); });
      slides[idx].classList.add('is-prev'); slides[idx].classList.remove('is-active');
      idx = (n + slides.length) % slides.length;
      var s = slides[idx]; s.classList.remove('is-prev');
      void s.offsetWidth; s.classList.add('is-active');
      if (cap) cap.textContent = s.dataset.cap || '';
      if (cnt) cnt.textContent = ('0' + (idx + 1)).slice(-2) + ' / ' + ('0' + slides.length).slice(-2);
      if (bar && !reduce) { bar.classList.remove('run'); void bar.offsetWidth; bar.classList.add('run'); }
    };
    if (slides.length) {
      slides[0].classList.add('is-active');
      if (cap) cap.textContent = slides[0].dataset.cap || '';
      if (bar && !reduce) setTimeout(function () { bar.classList.add('run'); }, 50);
      if (slides.length > 1 && !reduce) timer = setInterval(function () { show(idx + 1); }, 6500);
      document.addEventListener('visibilitychange', function () {
        clearInterval(timer);
        if (!document.hidden && slides.length > 1 && !reduce) timer = setInterval(function () { show(idx + 1); }, 6500);
      });
    }
  }

  /* ---------- scroll-driven scenes ---------- */
  var walk = $('[data-walk]'), rail = $('[data-rail]');
  var wide = window.innerWidth >= 900;
  if (walk && reduce) doc.classList.add('no-walk');
  if (rail && (reduce || !wide)) doc.classList.add('no-rail');
  var layers = walk ? $$('.walk__layer', walk) : [], steps = walk ? $$('.walk__step', walk) : [], ticks = walk ? $$('.walk__rail b', walk) : [];
  var track = rail ? $('.rail__track', rail) : null;
  var par = $$('[data-parallax]');

  function sizeRail() {
    if (!rail || doc.classList.contains('no-rail')) return;
    rail.style.height = (track.scrollWidth - window.innerWidth + window.innerHeight) + 'px';
  }
  sizeRail(); window.addEventListener('resize', sizeRail); window.addEventListener('load', sizeRail);

  function frame() {
    var vh = window.innerHeight, y = window.pageYOffset;
    if (hdr) { hdr.classList.toggle('is-hidden', y > lastY && y > 240 && !(menu && menu.classList.contains('is-open'))); lastY = y; }

    if (walk && !reduce) {
      var r = walk.getBoundingClientRect();
      var p = clamp(-r.top / (r.height - vh), 0, 1), seg = p * (layers.length - 1);
      layers.forEach(function (l, i) {
        var open = i === 0 ? 1 : ease(clamp(seg - (i - 1), 0, 1));
        var push = clamp(seg - i + (i === 0 ? 0 : 0), 0, 1);
        if (i > 0) l.style.clipPath = 'inset(' + ((1 - open) * 24) + '% ' + ((1 - open) * 38) + '% ' + ((1 - open) * 24) + '% ' + ((1 - open) * 38) + '%)';
        l.firstElementChild.style.transform = 'scale(' + (1.04 + push * 0.5 + (1 - open) * 0.12) + ')';
      });
      var on = Math.round(seg);
      steps.forEach(function (s, i) { s.classList.toggle('is-on', i === on); });
      ticks.forEach(function (b, i) { b.style.transform = 'scaleY(' + clamp(seg - i + 1, 0, 1) + ')'; });
    }

    if (rail && track && !doc.classList.contains('no-rail')) {
      var rr = rail.getBoundingClientRect();
      var rp = clamp(-rr.top / (rr.height - vh), 0, 1);
      track.style.transform = 'translate3d(' + (-rp * (track.scrollWidth - window.innerWidth)) + 'px,0,0)';
    }

    if (!reduce) par.forEach(function (el) {
      var b = el.getBoundingClientRect();
      if (b.bottom < -100 || b.top > vh + 100) return;
      var off = ((b.top + b.height / 2) - vh / 2) / vh;
      var img = el.querySelector('img');
      if (img) img.style.transform = 'translate3d(0,' + (off * -(parseFloat(el.dataset.parallax) || 60)) + 'px,0) scale(1.18)';
    });
    ticking = false;
  }
  var ticking = false;
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', req, { passive: true }); window.addEventListener('resize', req); frame();

  /* ---------- works filter ---------- */
  var filters = $$('[data-filter]'), grid = $('.wgrid');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.dataset.filter;
      filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      grid.classList.toggle('is-filtered', f !== 'all');
      $$('.tile', grid).forEach(function (t) {
        t.classList.toggle('is-out', f !== 'all' && t.dataset.cat !== f);
        t.classList.add('in');
      });
    });
  });

  /* ---------- contact form: composes an email ---------- */
  var form = $('[data-mailform]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form), lines = [];
    d.forEach(function (v, k) { if (v) lines.push(k + ': ' + v); });
    window.location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(form.dataset.subject + ' — ' + (d.get(form.dataset.namefield) || '')) +
      '&body=' + encodeURIComponent(lines.join('\n'));
    var st = $('[data-formstatus]'); if (st) st.hidden = false;
  });

  /* ---------- cursor ---------- */
  if (fine && !reduce) {
    var c = document.createElement('div'); c.className = 'cursor'; c.innerHTML = '<span></span>'; document.body.appendChild(c);
    var cx = -100, cy = -100, tx = -100, ty = -100, lab = c.firstChild;
    doc.classList.add('has-cursor');
    window.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    document.addEventListener('mouseover', function (e) {
      var t = e.target.closest ? e.target.closest('[data-cursor]') : null;
      c.classList.toggle('is-big', !!t); if (t) lab.textContent = t.dataset.cursor;
    });
    (function loop() { cx += (tx - cx) * .18; cy += (ty - cy) * .18; c.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)'; requestAnimationFrame(loop); })();
  }
})();
