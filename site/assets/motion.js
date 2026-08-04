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
    var els = [].slice.call(document.querySelectorAll('[data-reveal]'))
      .filter(function (e) { return !e.classList.contains('is-in'); });
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

  // Scroll work binds to the window, so it must bind once however many times
  // init runs. The frame functions re-query the DOM instead of capturing it,
  // which is what lets the same handlers serve a page swapped in later.
  var bound = false;

  function onScroll(frame) {
    var ticking = false;
    return function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { ticking = false; frame(); });
    };
  }

  // The artwork drifts a little slower than the page it sits in.
  function parallaxFrame() {
    if (REDUCED) return;
    var arts = [].slice.call(document.querySelectorAll('.scene > .art'));
    if (!arts.length) return;
    (function () {
      var vh = innerHeight;
      arts.forEach(function (art) {
        var r = art.parentNode.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var mid = (r.top + r.height / 2 - vh / 2) / vh;   // -1 .. 1 through view
        art.style.transform = 'translate3d(0,' + (mid * 26).toFixed(1) + 'px,0) scale(1.08)';
      });
    }());
  }

  // How far through the page you are. Cheap, passive, and the single
  // clearest signal that a long read has an end.
  function progressFrame() {
    var rail = document.querySelector('.progress span');
    if (!rail) return;
    var max = document.documentElement.scrollHeight - innerHeight;
    var pct = max > 40 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
    rail.style.width = (pct * 100).toFixed(2) + '%';
  }

  function scrollFrame() { parallaxFrame(); progressFrame(); }

  function init() {
    reveals();
    if (!bound) {
      bound = true;
      var handler = onScroll(scrollFrame);
      addEventListener('scroll', handler, { passive: true });
      addEventListener('resize', handler, { passive: true });
    }
    scrollFrame();
  }

  // Exposed so a host that swaps page content in place — the single-file
  // bundle — can re-run it without reloading the script or stacking listeners.
  window.contextInit = init;

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
}());
