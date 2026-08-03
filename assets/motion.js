/* ------------------------------------------------------------------
   Context — motion

   Two jobs. Reveal things as they arrive, and run the ambient canvas
   scenes that live inside every dark panel.

   Rules the whole file obeys:
   - nothing animates off-screen; an IntersectionObserver parks each scene
   - prefers-reduced-motion gets one static frame, not a frozen blank
   - every scene is deterministic from a seed, so a card looks the same
     on every load and the page does not shimmer on refresh
------------------------------------------------------------------- */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* -- a tiny seeded RNG, so scenes are stable between loads ---------- */
  function rng(seed) {
    var s = seed >>> 0 || 1;
    return function () {
      s ^= s << 13; s >>>= 0;
      s ^= s >> 17;
      s ^= s << 5;  s >>>= 0;
      return s / 4294967296;
    };
  }

  function hash(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }

  /* ---------------- scenes -------------------------------------------
     Each builds its state once from (w, h, rand) and returns a draw(ctx,
     t, w, h) where t is seconds. Colours come from the panel's own
     gradient, so a scene inherits whatever tone the story is in.
  -------------------------------------------------------------------- */

  var SCENES = {

    // drifting depth field — the default backdrop
    stars: function (w, h, rand) {
      var n = Math.min(190, Math.round(w * h / 5200)), pts = [];
      for (var i = 0; i < n; i++) {
        pts.push({
          x: rand(), y: rand(),
          z: 0.25 + rand() * 0.75,          // depth drives size, speed and alpha
          r: 0.5 + rand() * 1.9,
          tw: rand() * 6.28
        });
      }
      return function (c, t, w, h) {
        for (var i = 0; i < pts.length; i++) {
          var p = pts[i];
          var x = ((p.x + t * 0.006 * p.z) % 1.15 - 0.075) * w;
          var y = p.y * h;
          var a = (0.25 + p.z * 0.6) * (0.65 + 0.35 * Math.sin(t * 1.4 + p.tw));
          c.globalAlpha = a;
          c.beginPath();
          c.arc(x, y, p.r * p.z * 1.6, 0, 6.2832);
          c.fillStyle = '#fff';
          c.fill();
        }
        c.globalAlpha = 1;
      };
    },

    // the identity mark: one bright point, things going round it.
    // data-focus="x,y" moves the centre clear of the headline.
    orbit: function (w, h, rand, el) {
      var f = (el.getAttribute('data-focus') || '0.5,0.5').split(',').map(Number);
      var rings = [], bodies = [];
      for (var i = 0; i < 4; i++) rings.push({ r: 0.16 + i * 0.11, tilt: 0.34 + i * 0.05 });
      for (var j = 0; j < 7; j++) {
        bodies.push({
          ring: j % rings.length,
          a: rand() * 6.2832,
          sp: 0.12 + rand() * 0.3,
          size: 2.5 + rand() * 5
        });
      }
      return function (c, t, w, h) {
        var cx = w * f[0], cy = h * f[1], R = Math.min(w, h);
        rings.forEach(function (ring) {
          c.save();
          c.translate(cx, cy);
          c.scale(1, ring.tilt);
          c.beginPath();
          c.arc(0, 0, R * ring.r, 0, 6.2832);
          c.strokeStyle = 'rgba(255,255,255,.16)';
          c.lineWidth = 1;
          c.stroke();
          c.restore();
        });
        // the centre, breathing
        var pulse = 1 + Math.sin(t * 1.1) * 0.08;
        var g = c.createRadialGradient(cx, cy, 0, cx, cy, R * 0.12 * pulse);
        g.addColorStop(0, 'rgba(255,255,255,.95)');
        g.addColorStop(0.4, 'rgba(255,255,255,.35)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        c.fillStyle = g;
        c.beginPath();
        c.arc(cx, cy, R * 0.12 * pulse, 0, 6.2832);
        c.fill();

        bodies.forEach(function (b) {
          var ring = rings[b.ring];
          var a = b.a + t * b.sp;
          var x = cx + Math.cos(a) * R * ring.r;
          var y = cy + Math.sin(a) * R * ring.r * ring.tilt;
          c.beginPath();
          c.arc(x, y, b.size, 0, 6.2832);
          c.fillStyle = '#fff';
          c.globalAlpha = 0.9;
          c.fill();
          c.globalAlpha = 1;
        });
      };
    },

    // soft blobs sliding past each other — warm, organic, non-cosmic
    swarm: function (w, h, rand) {
      var n = 16, blobs = [];
      for (var i = 0; i < n; i++) {
        blobs.push({
          x: rand(), y: rand(),
          r: 0.06 + rand() * 0.16,
          sx: (rand() - 0.5) * 0.02,
          sy: (rand() - 0.5) * 0.02,
          ph: rand() * 6.28
        });
      }
      return function (c, t, w, h) {
        var R = Math.min(w, h);
        blobs.forEach(function (b) {
          var x = (b.x + Math.sin(t * 0.18 + b.ph) * 0.08 + t * b.sx) % 1.2 - 0.1;
          var y = (b.y + Math.cos(t * 0.15 + b.ph) * 0.08 + t * b.sy) % 1.2 - 0.1;
          var rr = b.r * R * (1 + Math.sin(t * 0.5 + b.ph) * 0.12);
          var g = c.createRadialGradient(x * w, y * h, 0, x * w, y * h, rr);
          g.addColorStop(0, 'rgba(255,255,255,.14)');
          g.addColorStop(1, 'rgba(255,255,255,0)');
          c.fillStyle = g;
          c.beginPath();
          c.arc(x * w, y * h, rr, 0, 6.2832);
          c.fill();
        });
      };
    },

    // layered sine bands — motion without any particles
    waves: function (w, h, rand) {
      var layers = [];
      for (var i = 0; i < 4; i++) {
        layers.push({ amp: 0.05 + i * 0.02, freq: 1.2 + i * 0.7, sp: 0.25 + i * 0.16, y: 0.42 + i * 0.13, a: 0.16 - i * 0.03 });
      }
      return function (c, t, w, h) {
        layers.forEach(function (L) {
          c.beginPath();
          c.moveTo(0, h);
          for (var x = 0; x <= w; x += 8) {
            var y = (L.y + Math.sin(x / w * 6.2832 * L.freq + t * L.sp) * L.amp) * h;
            c.lineTo(x, y);
          }
          c.lineTo(w, h);
          c.closePath();
          c.fillStyle = 'rgba(255,255,255,' + L.a + ')';
          c.fill();
        });
      };
    },

    // rings pushing outward from the centre — used for scale stories
    bloom: function (w, h, rand) {
      var n = 6;
      return function (c, t, w, h) {
        var cx = w * 0.5, cy = h * 0.55, R = Math.max(w, h) * 0.72;
        for (var i = 0; i < n; i++) {
          var f = ((t * 0.13) + i / n) % 1;
          c.beginPath();
          c.arc(cx, cy, f * R, 0, 6.2832);
          c.strokeStyle = 'rgba(255,255,255,' + (0.3 * (1 - f)).toFixed(3) + ')';
          c.lineWidth = 1.5;
          c.stroke();
        }
      };
    }
  };

  /* ---------------- runner -------------------------------------------- */

  function mount(el) {
    var name = el.getAttribute('data-scene');
    var build = SCENES[name];
    if (!build) return;

    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    el.insertBefore(canvas, el.firstChild);
    var c = canvas.getContext('2d');

    var draw = null, w = 0, h = 0, dpr = 1, running = false, raf = 0, t0 = 0;
    var seed = hash(name + (el.getAttribute('data-seed') || el.textContent.slice(0, 24)));

    function size() {
      var r = el.getBoundingClientRect();
      if (!r.width || !r.height) return false;
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = r.width; h = r.height;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      c.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw = build(w, h, rng(seed), el);
      return true;
    }

    function frame(ts) {
      if (!running) return;
      if (!t0) t0 = ts;
      c.clearRect(0, 0, w, h);
      draw(c, (ts - t0) / 1000, w, h);
      raf = requestAnimationFrame(frame);
    }

    function start() {
      if (running || !draw) return;
      if (REDUCED) { c.clearRect(0, 0, w, h); draw(c, 0, w, h); return; }
      running = true;
      raf = requestAnimationFrame(frame);
    }
    function stop() { running = false; cancelAnimationFrame(raf); }

    if (!size()) {
      // panel has no layout yet (hidden card, late font); try once more
      requestAnimationFrame(function () { if (size()) start(); });
    }

    var io = new IntersectionObserver(function (entries) {
      entries[0].isIntersecting ? start() : stop();
    }, { rootMargin: '120px' });
    io.observe(el);

    var rt;
    addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { stop(); t0 = 0; if (size()) start(); }, 180);
    });
  }

  /* ---------------- reveal on scroll ---------------------------------- */

  function reveals() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    if (REDUCED || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('is-in'); });
      return;
    }
    function reveal(el, delay) {
      setTimeout(function () { el.classList.add('is-in'); }, delay || 0);
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        // A jump — an anchor link, a restored scroll position, a flick on
        // mobile — can carry an element from below the fold to above it
        // without it ever intersecting. Reveal anything already passed,
        // otherwise that content stays invisible for good.
        var passed = !en.isIntersecting && en.boundingClientRect.top < 0;
        if (!en.isIntersecting && !passed) return;
        reveal(en.target, passed ? 0 : +(en.target.getAttribute('data-reveal') || 0));
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    els.forEach(function (e) {
      if (e.getBoundingClientRect().bottom < 0) { reveal(e, 0); return; }
      io.observe(e);
    });
  }

  /* ---------------- pointer parallax on the hero ----------------------- */

  function parallax() {
    if (REDUCED) return;
    var hosts = document.querySelectorAll('[data-parallax]');
    if (!hosts.length) return;
    addEventListener('pointermove', function (e) {
      var x = (e.clientX / innerWidth - 0.5), y = (e.clientY / innerHeight - 0.5);
      hosts.forEach(function (host) {
        var d = +(host.getAttribute('data-parallax') || 12);
        host.style.transform = 'translate3d(' + (-x * d).toFixed(2) + 'px,' + (-y * d).toFixed(2) + 'px,0)';
      });
    }, { passive: true });
  }

  function init() {
    document.querySelectorAll('[data-scene]').forEach(mount);
    reveals();
    parallax();
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
}());
