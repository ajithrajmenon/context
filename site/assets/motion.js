/* ------------------------------------------------------------------
   Context — motion

   The artwork is generated SVG and animates itself in CSS, so this file
   only handles the page: revealing cards as they arrive, and a little
   parallax on the illustrations behind the heroes.
------------------------------------------------------------------- */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function reveals() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    if (REDUCED || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('is-in'); });
      return;
    }
    function show(el, d) { setTimeout(function () { el.classList.add('is-in'); }, d || 0); }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        // A jump — an anchor link, a restored scroll position, a fast flick
        // on mobile — can carry an element from below the fold to above it
        // without it ever intersecting. Reveal anything already passed, or
        // that content stays invisible for good.
        var passed = !en.isIntersecting && en.boundingClientRect.top < 0;
        if (!en.isIntersecting && !passed) return;
        show(en.target, passed ? 0 : +(en.target.getAttribute('data-reveal') || 0));
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: .06 });

    els.forEach(function (e) {
      if (e.getBoundingClientRect().bottom < 0) { show(e, 0); return; }
      io.observe(e);
    });
  }

  // The artwork drifts a little slower than the page it sits in.
  function parallax() {
    if (REDUCED) return;
    var arts = [].slice.call(document.querySelectorAll('.scene > .art'));
    if (!arts.length) return;
    var ticking = false;

    function frame() {
      ticking = false;
      var vh = innerHeight;
      arts.forEach(function (art) {
        var r = art.parentNode.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var mid = (r.top + r.height / 2 - vh / 2) / vh;   // -1 .. 1 through view
        art.style.transform = 'translate3d(0,' + (mid * 26).toFixed(1) + 'px,0) scale(1.08)';
      });
    }
    addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }, { passive: true });
    frame();
  }

  // How far through the page you are. Cheap, passive, and the single
  // clearest signal that a long read has an end.
  function progress() {
    var rail = document.querySelector('.progress span');
    if (!rail) return;
    var ticking = false;
    function frame() {
      ticking = false;
      var max = document.documentElement.scrollHeight - innerHeight;
      var pct = max > 40 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
      rail.style.width = (pct * 100).toFixed(2) + '%';
    }
    addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }, { passive: true });
    addEventListener('resize', frame, { passive: true });
    frame();
  }

  function init() { reveals(); parallax(); progress(); }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
}());
