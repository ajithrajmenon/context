/* ------------------------------------------------------------------
   Context — motion

   Two jobs. Reveal cards as they arrive, and run the canvas scenes that
   do most of the explaining. A story stacks several of these, so the
   engine has to stay cheap.

   Rules the whole file obeys:
   - nothing animates off-screen; an IntersectionObserver parks each scene
   - prefers-reduced-motion gets one static frame, never a frozen blank
   - scenes are seeded, so a card looks identical on every load
   - scenes draw in white only; the card's own gradient supplies the hue,
     which is what lets one story walk through several tones
------------------------------------------------------------------- */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TAU = 6.283185;

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

  // Point counts scale with panel area, but a card is a fraction of a hero.
  // Without a floor, small panels end up with a handful of points and can
  // look empty — especially in scenes where some of them switch off.
  function count(w, h, per, min, max) {
    return Math.max(min, Math.min(max, Math.round(w * h / per)));
  }

  function dot(c, x, y, r, a) {
    c.globalAlpha = a;
    c.beginPath();
    c.arc(x, y, r, 0, TAU);
    c.fillStyle = '#fff';
    c.fill();
    c.globalAlpha = 1;
  }

  /* ---------------- scenes ---------------------------------------- */

  var SCENES = {

    // depth field, drifting
    stars: function (w, h, rand) {
      var n = count(w, h, 5200, 55, 190), pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: rand(), y: rand(), z: .25 + rand() * .75, r: .5 + rand() * 1.9, tw: rand() * TAU });
      return function (c, t, w, h) {
        pts.forEach(function (p) {
          var x = ((p.x + t * .006 * p.z) % 1.15 - .075) * w;
          dot(c, x, p.y * h, p.r * p.z * 1.6, (.25 + p.z * .6) * (.65 + .35 * Math.sin(t * 1.4 + p.tw)));
        });
      };
    },

    // one bright point, things going round it — the house mark
    orbit: function (w, h, rand, el) {
      var f = (el.getAttribute('data-focus') || '0.5,0.5').split(',').map(Number);
      var rings = [], bodies = [];
      for (var i = 0; i < 4; i++) rings.push({ r: .16 + i * .11, tilt: .34 + i * .05 });
      for (var j = 0; j < 7; j++) bodies.push({ ring: j % 4, a: rand() * TAU, sp: .12 + rand() * .3, size: 2.5 + rand() * 5 });
      return function (c, t, w, h) {
        var cx = w * f[0], cy = h * f[1], R = Math.min(w, h);
        rings.forEach(function (ring) {
          c.save(); c.translate(cx, cy); c.scale(1, ring.tilt);
          c.beginPath(); c.arc(0, 0, R * ring.r, 0, TAU);
          c.strokeStyle = 'rgba(255,255,255,.16)'; c.lineWidth = 1; c.stroke();
          c.restore();
        });
        var pulse = 1 + Math.sin(t * 1.1) * .08, gr = R * .12 * pulse;
        var g = c.createRadialGradient(cx, cy, 0, cx, cy, gr);
        g.addColorStop(0, 'rgba(255,255,255,.95)');
        g.addColorStop(.4, 'rgba(255,255,255,.35)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        c.fillStyle = g; c.beginPath(); c.arc(cx, cy, gr, 0, TAU); c.fill();
        bodies.forEach(function (b) {
          var ring = rings[b.ring], a = b.a + t * b.sp;
          dot(c, cx + Math.cos(a) * R * ring.r, cy + Math.sin(a) * R * ring.r * ring.tilt, b.size, .9);
        });
      };
    },

    // soft blobs sliding past each other
    swarm: function (w, h, rand) {
      var blobs = [];
      for (var i = 0; i < 16; i++) blobs.push({ x: rand(), y: rand(), r: .06 + rand() * .16, sx: (rand() - .5) * .02, sy: (rand() - .5) * .02, ph: rand() * TAU });
      return function (c, t, w, h) {
        var R = Math.min(w, h);
        blobs.forEach(function (b) {
          var x = (b.x + Math.sin(t * .18 + b.ph) * .08 + t * b.sx) % 1.2 - .1;
          var y = (b.y + Math.cos(t * .15 + b.ph) * .08 + t * b.sy) % 1.2 - .1;
          var rr = b.r * R * (1 + Math.sin(t * .5 + b.ph) * .12);
          var g = c.createRadialGradient(x * w, y * h, 0, x * w, y * h, rr);
          g.addColorStop(0, 'rgba(255,255,255,.14)');
          g.addColorStop(1, 'rgba(255,255,255,0)');
          c.fillStyle = g; c.beginPath(); c.arc(x * w, y * h, rr, 0, TAU); c.fill();
        });
      };
    },

    waves: function (w, h, rand) {
      var layers = [];
      for (var i = 0; i < 4; i++) layers.push({ amp: .05 + i * .02, freq: 1.2 + i * .7, sp: .25 + i * .16, y: .42 + i * .13, a: .16 - i * .03 });
      return function (c, t, w, h) {
        layers.forEach(function (L) {
          c.beginPath(); c.moveTo(0, h);
          for (var x = 0; x <= w; x += 8) c.lineTo(x, (L.y + Math.sin(x / w * TAU * L.freq + t * L.sp) * L.amp) * h);
          c.lineTo(w, h); c.closePath();
          c.fillStyle = 'rgba(255,255,255,' + L.a + ')'; c.fill();
        });
      };
    },

    bloom: function (w, h, rand) {
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .55, R = Math.max(w, h) * .72;
        for (var i = 0; i < 6; i++) {
          var f = ((t * .13) + i / 6) % 1;
          c.beginPath(); c.arc(cx, cy, f * R, 0, TAU);
          c.strokeStyle = 'rgba(255,255,255,' + (.3 * (1 - f)).toFixed(3) + ')';
          c.lineWidth = 1.5; c.stroke();
        }
      };
    },

    /* --- scenes written for particular stories --------------------- */

    // a tidy grid falls apart and never tidies itself — the arrow of time
    entropy: function (w, h, rand) {
      var cols = 16, rows = 8, pts = [];
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        pts.push({ hx: (x + .5) / cols, hy: (y + .5) / rows, dx: (rand() - .5), dy: (rand() - .5), ph: rand() * TAU });
      }
      return function (c, t, w, h) {
        var f = (t * .1) % 2;                        // 0..1 tidy->messy, then hold
        var k = f < 1 ? f : 1;
        k = k * k * (3 - 2 * k);                      // ease
        pts.forEach(function (p) {
          var x = (p.hx + p.dx * .42 * k) * w;
          var y = (p.hy + p.dy * .42 * k) * h;
          dot(c, x, y, 3, .28 + .5 * (1 - k * .5));
        });
      };
    },

    // everything moving away from everything else, with no centre
    expand: function (w, h, rand) {
      var pts = [];
      for (var i = 0; i < 46; i++) pts.push({ x: rand() - .5, y: rand() - .5, r: 1.5 + rand() * 3 });
      return function (c, t, w, h) {
        var s = 1 + ((t * .12) % 1) * 1.6;
        var fade = 1 - ((t * .12) % 1);
        pts.forEach(function (p) {
          var x = w * .5 + p.x * w * s, y = h * .5 + p.y * h * s;
          if (x < -20 || x > w + 20 || y < -20 || y > h + 20) return;
          dot(c, x, y, p.r, .2 + fade * .6);
        });
      };
    },

    // a speck of nucleus in an enormous amount of nothing
    atom: function (w, h, rand) {
      var shells = [{ r: .2, n: 2, sp: .55 }, { r: .32, n: 4, sp: -.36 }, { r: .43, n: 3, sp: .24 }];
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .5, R = Math.min(w, h);
        shells.forEach(function (s) {
          c.beginPath(); c.arc(cx, cy, R * s.r, 0, TAU);
          c.strokeStyle = 'rgba(255,255,255,.12)'; c.lineWidth = 1; c.stroke();
          for (var i = 0; i < s.n; i++) {
            var a = t * s.sp + i * TAU / s.n;
            dot(c, cx + Math.cos(a) * R * s.r, cy + Math.sin(a) * R * s.r, 3.5, .85);
          }
        });
        // the nucleus is deliberately almost too small to see
        var g = c.createRadialGradient(cx, cy, 0, cx, cy, R * .05);
        g.addColorStop(0, 'rgba(255,255,255,.95)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        c.fillStyle = g; c.beginPath(); c.arc(cx, cy, R * .05, 0, TAU); c.fill();
        dot(c, cx, cy, Math.max(1.6, R * .006), 1);
      };
    },

    // cells drifting; a few flare as something finds them
    cells: function (w, h, rand) {
      var cs = [];
      for (var i = 0; i < 26; i++) cs.push({ x: rand(), y: rand(), r: 5 + rand() * 13, sp: .01 + rand() * .03, ph: rand() * TAU, hot: rand() < .22 });
      return function (c, t, w, h) {
        cs.forEach(function (b) {
          var x = ((b.x + t * b.sp) % 1.1 - .05) * w;
          var y = (b.y + Math.sin(t * .35 + b.ph) * .05) * h;
          var flare = b.hot ? (.5 + .5 * Math.sin(t * 2.2 + b.ph)) : 0;
          c.beginPath(); c.arc(x, y, b.r * (1 + flare * .18), 0, TAU);
          c.strokeStyle = 'rgba(255,255,255,' + (.22 + flare * .55) + ')';
          c.lineWidth = 1.6; c.stroke();
          if (b.hot) dot(c, x, y, b.r * .3, .25 + flare * .5);
        });
      };
    },

    // rays crossing the panel, always at the same speed
    beam: function (w, h, rand) {
      var rays = [];
      for (var i = 0; i < 22; i++) rays.push({ y: rand(), off: rand(), len: .12 + rand() * .22, a: .2 + rand() * .5 });
      return function (c, t, w, h) {
        rays.forEach(function (r) {
          var x = ((r.off + t * .22) % 1.3 - .15) * w;
          var L = r.len * w;
          var g = c.createLinearGradient(x, 0, x + L, 0);
          g.addColorStop(0, 'rgba(255,255,255,0)');
          g.addColorStop(.5, 'rgba(255,255,255,' + r.a + ')');
          g.addColorStop(1, 'rgba(255,255,255,0)');
          c.strokeStyle = g; c.lineWidth = 2; c.lineCap = 'round';
          c.beginPath(); c.moveTo(x, r.y * h); c.lineTo(x + L, r.y * h); c.stroke();
        });
      };
    },

    // a grid of space, dented by something heavy sitting on it
    grid: function (w, h, rand) {
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .56;
        var depth = 1 + Math.sin(t * .5) * .18;
        c.strokeStyle = 'rgba(255,255,255,.2)';
        c.lineWidth = 1;
        function warp(x, y) {
          var dx = x - cx, dy = (y - cy) * 1.9;
          var d = Math.sqrt(dx * dx + dy * dy) + 24;
          var pull = Math.min(h * .3, (h * 5200 * depth) / (d * d));
          return y + pull;
        }
        for (var gy = 0; gy <= 9; gy++) {
          c.beginPath();
          for (var x = 0; x <= w; x += 10) {
            var y = warp(x, (gy / 9) * h);
            x ? c.lineTo(x, y) : c.moveTo(x, y);
          }
          c.stroke();
        }
        for (var gx = 0; gx <= 14; gx++) {
          var px = (gx / 14) * w;
          c.beginPath();
          for (var yy = 0; yy <= h; yy += 10) {
            var wy = warp(px, yy);
            yy ? c.lineTo(px, wy) : c.moveTo(px, wy);
          }
          c.stroke();
        }
        dot(c, cx, warp(cx, cy) - h * .02, 9, .95);
      };
    },

    // pairs popping out of nothing and cancelling again
    flicker: function (w, h, rand) {
      var pairs = [];
      for (var i = 0; i < 26; i++) pairs.push({ x: rand(), y: rand(), t0: rand() * 3, life: .5 + rand() * .9, gap: 6 + rand() * 14 });
      return function (c, t, w, h) {
        pairs.forEach(function (p) {
          var age = (t - p.t0) % 3;
          if (age < 0 || age > p.life) return;
          var f = age / p.life;
          var sep = Math.sin(f * Math.PI) * p.gap;
          var a = Math.sin(f * Math.PI) * .85;
          dot(c, p.x * w - sep, p.y * h, 2.6, a);
          dot(c, p.x * w + sep, p.y * h, 2.6, a);
        });
      };
    },

    // the lights going out, one at a time, and not coming back
    dying: function (w, h, rand) {
      var n = count(w, h, 6000, 60, 150), pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: rand(), y: rand(), r: .6 + rand() * 2.1, out: rand() });
      return function (c, t, w, h) {
        // Sweeps out most of the field, then holds. Capped below 1 on purpose:
        // a handful of long-lived stars survive, which is both true and keeps
        // the panel from going completely blank and reading as broken.
        var k = Math.min((t * .05) % 1.35, .88);
        pts.forEach(function (p) {
          if (p.out < k) return;                     // this one has gone out
          dot(c, p.x * w, p.y * h, p.r, .3 + .55 * (1 - k));
        });
      };
    },

    // every piece swapped out, one by one, and it is still the same shape
    replace: function (w, h, rand) {
      var cols = 14, rows = 7, cells = [];
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) cells.push({ x: (x + .5) / cols, y: (y + .5) / rows, when: rand() });
      return function (c, t, w, h) {
        var k = (t * .09) % 1;
        cells.forEach(function (p) {
          var swapped = p.when < k;
          var d = Math.abs(p.when - k);
          var flash = d < .05 ? (1 - d / .05) : 0;
          c.beginPath();
          c.arc(p.x * w, p.y * h, 5 + flash * 4, 0, TAU);
          if (swapped) { c.fillStyle = 'rgba(255,255,255,' + (.5 + flash * .5) + ')'; c.fill(); }
          else { c.strokeStyle = 'rgba(255,255,255,.32)'; c.lineWidth = 1.4; c.stroke(); }
        });
      };
    }
  };

  /* ---------------- runner ---------------------------------------- */

  function mount(el) {
    var build = SCENES[el.getAttribute('data-scene')];
    if (!build) return;

    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    el.insertBefore(canvas, el.firstChild);
    var c = canvas.getContext('2d');

    var draw = null, w = 0, h = 0, running = false, raf = 0, t0 = 0;
    var seed = hash(el.getAttribute('data-scene') + (el.getAttribute('data-seed') || ''));

    function size() {
      var r = el.getBoundingClientRect();
      if (!r.width || !r.height) return false;
      var dpr = Math.min(devicePixelRatio || 1, 2);
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
      if (!draw || running) return;
      if (REDUCED) { c.clearRect(0, 0, w, h); draw(c, 1.2, w, h); return; }
      running = true;
      raf = requestAnimationFrame(frame);
    }
    function stop() { running = false; cancelAnimationFrame(raf); }

    if (!size()) requestAnimationFrame(function () { if (size()) start(); });

    new IntersectionObserver(function (e) {
      e[0].isIntersecting ? start() : stop();
    }, { rootMargin: '150px' }).observe(el);

    var rt;
    addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { stop(); t0 = 0; if (size()) start(); }, 180);
    });
  }

  /* ---------------- reveals --------------------------------------- */

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
        // A jump — anchor link, restored scroll, a fast flick — can carry an
        // element from below the fold to above it without ever intersecting.
        // Reveal anything already passed, or that content is gone for good.
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

  function init() {
    document.querySelectorAll('[data-scene]').forEach(mount);
    reveals();
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
}());
