/* ------------------------------------------------------------------
   Context — motion

   Scenes do the explaining. Two rules they all follow:

   1. MULTICOLOUR. A scene carries many hues at once, from the shared
      palette below. The card's gradient is the lighting; the scene is
      the life on top of it. One flat hue per panel reads as decoration.

   2. LITERAL. Every scene draws its own subject. The ant story gets
      ants and trails, the virus story gets virus particles docking to a
      cell. No scene is chosen because it looks nice.

   Engine rules:
   - nothing animates off-screen; an IntersectionObserver parks each scene
   - prefers-reduced-motion gets one composed static frame, never a blank
   - scenes are seeded, so a card looks identical on every load
   - point counts have a floor as well as a ceiling, or small cards go sparse
------------------------------------------------------------------- */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TAU = 6.283185;

  /* The house palette. Every colour is light enough to sit on a dark
     panel, and saturated enough to hold its own next to the others. */
  var PAL = {
    cyan:    '#22D3EE',
    lime:    '#A3E635',
    magenta: '#F472B6',
    violet:  '#A78BFA',
    amber:   '#FBBF24',
    emerald: '#34D399',
    coral:   '#FB7185',
    sky:     '#60A5FA',
    orchid:  '#C084FC',
    teal:    '#2DD4BF',
    gold:    '#FCD34D',
    white:   '#FFFFFF'
  };
  var SPREAD = [PAL.cyan, PAL.lime, PAL.magenta, PAL.violet, PAL.amber,
                PAL.emerald, PAL.coral, PAL.sky, PAL.orchid, PAL.teal];

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

  // A card is a fraction of a hero's area. Without a floor, small panels
  // end up with a handful of points and read as broken.
  function count(w, h, per, min, max) {
    return Math.max(min, Math.min(max, Math.round(w * h / per)));
  }

  function disc(c, x, y, r, col, a) {
    c.globalAlpha = a === undefined ? 1 : a;
    c.beginPath();
    c.arc(x, y, r, 0, TAU);
    c.fillStyle = col;
    c.fill();
    c.globalAlpha = 1;
  }

  function ring(c, x, y, r, col, a, lw) {
    c.globalAlpha = a === undefined ? 1 : a;
    c.beginPath();
    c.arc(x, y, r, 0, TAU);
    c.strokeStyle = col;
    c.lineWidth = lw || 2;
    c.stroke();
    c.globalAlpha = 1;
  }

  function glow(c, x, y, r, col, a) {
    var g = c.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, col);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    c.globalAlpha = a === undefined ? .5 : a;
    c.fillStyle = g;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    c.globalAlpha = 1;
  }

  /* ================= scenes ======================================== */

  var SCENES = {

    /* --- space ---------------------------------------------------- */

    // real stars are not white: blue giants through to red dwarfs
    stars: function (w, h, rand) {
      var COL = [PAL.sky, PAL.white, PAL.gold, PAL.amber, PAL.coral, PAL.cyan];
      var n = count(w, h, 5200, 55, 190), pts = [];
      for (var i = 0; i < n; i++) {
        pts.push({ x: rand(), y: rand(), z: .25 + rand() * .75, r: .6 + rand() * 2.1,
                   tw: rand() * TAU, col: COL[(rand() * COL.length) | 0] });
      }
      return function (c, t, w, h) {
        pts.forEach(function (p) {
          var x = ((p.x + t * .006 * p.z) % 1.15 - .075) * w;
          var a = (.3 + p.z * .6) * (.6 + .4 * Math.sin(t * 1.4 + p.tw));
          disc(c, x, p.y * h, p.r * p.z * 1.7, p.col, a);
        });
      };
    },

    // a star with planets, each its own world
    orbit: function (w, h, rand, el) {
      var f = (el.getAttribute('data-focus') || '0.5,0.5').split(',').map(Number);
      var COL = [PAL.cyan, PAL.coral, PAL.lime, PAL.violet, PAL.amber, PAL.teal, PAL.magenta];
      var rings = [], bodies = [];
      for (var i = 0; i < 4; i++) rings.push({ r: .16 + i * .11, tilt: .34 + i * .05, col: SPREAD[i * 2] });
      for (var j = 0; j < 7; j++) {
        bodies.push({ ring: j % 4, a: rand() * TAU, sp: .12 + rand() * .3,
                      size: 3 + rand() * 5, col: COL[j % COL.length] });
      }
      return function (c, t, w, h) {
        var cx = w * f[0], cy = h * f[1], R = Math.min(w, h);
        rings.forEach(function (rg) {
          c.save(); c.translate(cx, cy); c.scale(1, rg.tilt);
          ring(c, 0, 0, R * rg.r, rg.col, .28, 1.2);
          c.restore();
        });
        var pulse = 1 + Math.sin(t * 1.1) * .08;
        glow(c, cx, cy, R * .17 * pulse, PAL.gold, .75);
        disc(c, cx, cy, R * .045 * pulse, PAL.white, 1);
        bodies.forEach(function (b) {
          var rg = rings[b.ring], a = b.a + t * b.sp;
          var x = cx + Math.cos(a) * R * rg.r, y = cy + Math.sin(a) * R * rg.r * rg.tilt;
          glow(c, x, y, b.size * 3, b.col, .4);
          disc(c, x, y, b.size, b.col, 1);
        });
      };
    },

    // galaxies of different types drifting apart from each other
    expand: function (w, h, rand) {
      var pts = [];
      for (var i = 0; i < 74; i++) {
        pts.push({ x: rand() - .5, y: rand() - .5, r: 2 + rand() * 4,
                   col: SPREAD[(rand() * SPREAD.length) | 0] });
      }
      return function (c, t, w, h) {
        var k = (t * .12) % 1, s = 1 + k * 1.6, fade = 1 - k;
        pts.forEach(function (p) {
          var x = w * .5 + p.x * w * s, y = h * .5 + p.y * h * s;
          if (x < -30 || x > w + 30 || y < -30 || y > h + 30) return;
          glow(c, x, y, p.r * 4, p.col, .25 * fade + .12);
          disc(c, x, y, p.r, p.col, .35 + fade * .6);
        });
      };
    },

    // stars burning out; the small red ones outlast everything
    dying: function (w, h, rand) {
      var HOT = [PAL.sky, PAL.white, PAL.cyan, PAL.gold];
      var n = count(w, h, 6000, 60, 150), pts = [];
      for (var i = 0; i < n; i++) {
        var cool = rand();
        pts.push({ x: rand(), y: rand(), r: .8 + rand() * 2.2, out: cool,
                   // the ones that survive longest are the cool red dwarfs
                   col: cool > .8 ? PAL.coral : HOT[(rand() * HOT.length) | 0] });
      }
      return function (c, t, w, h) {
        var k = Math.min((t * .05) % 1.35, .88);
        pts.forEach(function (p) {
          if (p.out < k) return;
          disc(c, p.x * w, p.y * h, p.r, p.col, .35 + .55 * (1 - k));
        });
      };
    },

    // space as a sheet, dented by something heavy
    grid: function (w, h, rand) {
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .56, depth = 1 + Math.sin(t * .5) * .18;
        function warp(x, y) {
          var dx = x - cx, dy = (y - cy) * 1.9;
          var d = Math.sqrt(dx * dx + dy * dy) + 24;
          return y + Math.min(h * .3, (h * 5200 * depth) / (d * d));
        }
        for (var gy = 0; gy <= 9; gy++) {
          c.beginPath();
          for (var x = 0; x <= w; x += 10) {
            var y = warp(x, (gy / 9) * h);
            x ? c.lineTo(x, y) : c.moveTo(x, y);
          }
          c.strokeStyle = gy % 2 ? PAL.cyan : PAL.violet;
          c.globalAlpha = .3; c.lineWidth = 1; c.stroke(); c.globalAlpha = 1;
        }
        for (var gx = 0; gx <= 14; gx++) {
          var px = (gx / 14) * w;
          c.beginPath();
          for (var yy = 0; yy <= h; yy += 10) {
            var wy = warp(px, yy);
            yy ? c.lineTo(px, wy) : c.moveTo(px, wy);
          }
          c.strokeStyle = gx % 2 ? PAL.teal : PAL.sky;
          c.globalAlpha = .22; c.stroke(); c.globalAlpha = 1;
        }
        glow(c, cx, warp(cx, cy) - h * .02, 34, PAL.amber, .55);
        disc(c, cx, warp(cx, cy) - h * .02, 10, PAL.gold, 1);
      };
    },

    // light, split into the colours it is actually made of
    beam: function (w, h, rand) {
      var COL = [PAL.coral, PAL.amber, PAL.lime, PAL.emerald, PAL.cyan, PAL.sky, PAL.orchid];
      var rays = [];
      for (var i = 0; i < 26; i++) {
        rays.push({ y: rand(), off: rand(), len: .14 + rand() * .24,
                    a: .35 + rand() * .5, col: COL[i % COL.length] });
      }
      return function (c, t, w, h) {
        rays.forEach(function (r) {
          var x = ((r.off + t * .22) % 1.3 - .15) * w, L = r.len * w;
          var g = c.createLinearGradient(x, 0, x + L, 0);
          g.addColorStop(0, 'rgba(0,0,0,0)');
          g.addColorStop(.5, r.col);
          g.addColorStop(1, 'rgba(0,0,0,0)');
          c.globalAlpha = r.a; c.strokeStyle = g; c.lineWidth = 2.4; c.lineCap = 'round';
          c.beginPath(); c.moveTo(x, r.y * h); c.lineTo(x + L, r.y * h); c.stroke();
          c.globalAlpha = 1;
        });
      };
    },

    /* --- matter and time ------------------------------------------ */

    // coloured blocks in a tidy row, scattering and never coming back
    entropy: function (w, h, rand) {
      var cols = 16, rows = 8, pts = [];
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        pts.push({ hx: (x + .5) / cols, hy: (y + .5) / rows,
                   dx: rand() - .5, dy: rand() - .5,
                   col: SPREAD[(x + y) % SPREAD.length] });
      }
      return function (c, t, w, h) {
        var f = (t * .1) % 2, k = f < 1 ? f : 1;
        k = k * k * (3 - 2 * k);
        pts.forEach(function (p) {
          disc(c, (p.hx + p.dx * .42 * k) * w, (p.hy + p.dy * .42 * k) * h,
               3.4, p.col, .55 + .4 * (1 - k));
        });
      };
    },

    // a speck of nucleus, an enormous gap, and electrons a long way out
    atom: function (w, h, rand) {
      var shells = [{ r: .2, n: 2, sp: .55, col: PAL.cyan },
                    { r: .32, n: 4, sp: -.36, col: PAL.lime },
                    { r: .43, n: 3, sp: .24, col: PAL.violet }];
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .5, R = Math.min(w, h);
        shells.forEach(function (s) {
          ring(c, cx, cy, R * s.r, s.col, .2, 1);
          for (var i = 0; i < s.n; i++) {
            var a = t * s.sp + i * TAU / s.n;
            var x = cx + Math.cos(a) * R * s.r, y = cy + Math.sin(a) * R * s.r;
            glow(c, x, y, 13, s.col, .45);
            disc(c, x, y, 3.6, s.col, 1);
          }
        });
        glow(c, cx, cy, R * .07, PAL.magenta, .8);
        disc(c, cx, cy, Math.max(1.8, R * .008), PAL.magenta, 1);
      };
    },

    // matter and antimatter, borrowed from nothing and paid straight back
    flicker: function (w, h, rand) {
      var pairs = [];
      for (var i = 0; i < 44; i++) {
        var j = (rand() * 5) | 0;
        pairs.push({ x: rand(), y: rand(), t0: rand() * 3, life: .5 + rand() * .9,
                     gap: 7 + rand() * 15,
                     a: [PAL.cyan, PAL.lime, PAL.amber, PAL.violet, PAL.teal][j],
                     b: [PAL.magenta, PAL.coral, PAL.orchid, PAL.gold, PAL.sky][j] });
      }
      return function (c, t, w, h) {
        pairs.forEach(function (p) {
          var age = (t - p.t0) % 3;
          if (age < 0 || age > p.life) return;
          var f = age / p.life, sep = Math.sin(f * Math.PI) * p.gap;
          var al = Math.sin(f * Math.PI);
          disc(c, p.x * w - sep, p.y * h, 3, p.a, al);
          disc(c, p.x * w + sep, p.y * h, 3, p.b, al);
        });
      };
    },

    // rings pushing outward, each a different colour
    bloom: function (w, h, rand) {
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .55, R = Math.max(w, h) * .72;
        for (var i = 0; i < 7; i++) {
          var f = ((t * .13) + i / 7) % 1;
          ring(c, cx, cy, f * R, SPREAD[i], .45 * (1 - f), 2);
        }
      };
    },

    waves: function (w, h, rand) {
      var COL = [PAL.violet, PAL.magenta, PAL.cyan, PAL.teal, PAL.sky];
      var layers = [];
      for (var i = 0; i < 5; i++) {
        layers.push({ amp: .05 + i * .018, freq: 1.2 + i * .7, sp: .25 + i * .16,
                      y: .38 + i * .12, a: .3 - i * .04, col: COL[i] });
      }
      return function (c, t, w, h) {
        layers.forEach(function (L) {
          c.beginPath(); c.moveTo(0, h);
          for (var x = 0; x <= w; x += 8) c.lineTo(x, (L.y + Math.sin(x / w * TAU * L.freq + t * L.sp) * L.amp) * h);
          c.lineTo(w, h); c.closePath();
          c.globalAlpha = L.a; c.fillStyle = L.col; c.fill(); c.globalAlpha = 1;
        });
      };
    },

    /* --- life ------------------------------------------------------ */

    // a crowd of microbes, no two the same
    swarm: function (w, h, rand) {
      var blobs = [];
      for (var i = 0; i < 30; i++) {
        blobs.push({ x: rand(), y: rand(), r: .05 + rand() * .13,
                     sx: (rand() - .5) * .02, sy: (rand() - .5) * .02,
                     ph: rand() * TAU, col: SPREAD[(rand() * SPREAD.length) | 0] });
      }
      return function (c, t, w, h) {
        var R = Math.min(w, h);
        blobs.forEach(function (b) {
          var x = ((b.x + Math.sin(t * .18 + b.ph) * .08 + t * b.sx) % 1.2 - .1) * w;
          var y = ((b.y + Math.cos(t * .15 + b.ph) * .08 + t * b.sy) % 1.2 - .1) * h;
          var rr = b.r * R * (1 + Math.sin(t * .5 + b.ph) * .12);
          glow(c, x, y, rr, b.col, .3);
          disc(c, x, y, rr * .3, b.col, .55);
        });
      };
    },

    // immune cells hunting invaders and swallowing them
    cells: function (w, h, rand) {
      var defenders = [], germs = [];
      for (var i = 0; i < 13; i++) {
        defenders.push({ x: rand(), y: rand(), r: 13 + rand() * 12, sp: .012 + rand() * .022,
                         ph: rand() * TAU, col: i % 2 ? PAL.cyan : PAL.teal });
      }
      for (var j = 0; j < 26; j++) {
        germs.push({ x: rand(), y: rand(), r: 4 + rand() * 4, ph: rand() * TAU,
                     col: j % 3 === 0 ? PAL.magenta : j % 3 === 1 ? PAL.coral : PAL.orchid,
                     eaten: rand() * 6 });
      }
      return function (c, t, w, h) {
        germs.forEach(function (g) {
          var cycle = (t + g.eaten) % 6;
          if (cycle > 4.6) return;                       // caught and gone
          var a = cycle > 4 ? (4.6 - cycle) / .6 : 1;
          var x = ((g.x + Math.sin(t * .3 + g.ph) * .05) % 1) * w;
          var y = ((g.y + Math.cos(t * .27 + g.ph) * .05) % 1) * h;
          disc(c, x, y, g.r, g.col, .9 * a);
          glow(c, x, y, g.r * 3, g.col, .28 * a);
        });
        defenders.forEach(function (d) {
          var x = ((d.x + t * d.sp) % 1.15 - .07) * w;
          var y = (d.y + Math.sin(t * .4 + d.ph) * .06) * h;
          var breathe = 1 + Math.sin(t * 1.6 + d.ph) * .1;
          glow(c, x, y, d.r * 2.4 * breathe, d.col, .3);
          ring(c, x, y, d.r * breathe, d.col, .85, 2.4);
          disc(c, x, y, d.r * .3, PAL.lime, .8);          // the nucleus
        });
      };
    },

    // virus particles docking onto a cell and taking it over
    virus: function (w, h, rand) {
      var vs = [];
      for (var i = 0; i < 18; i++) {
        vs.push({ a: rand() * TAU, d: .55 + rand() * .5, sp: .04 + rand() * .05,
                  r: 6 + rand() * 4, col: i % 3 === 0 ? PAL.magenta : i % 3 === 1 ? PAL.coral : PAL.orchid,
                  spikes: 7 + ((rand() * 4) | 0) });
      }
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .52, R = Math.min(w, h) * .22;
        // the cell being targeted
        glow(c, cx, cy, R * 2, PAL.cyan, .28);
        ring(c, cx, cy, R, PAL.cyan, .8, 3);
        disc(c, cx, cy, R * .3, PAL.lime, .55);
        vs.forEach(function (v) {
          var d = Math.max(1, v.d - (t * v.sp) % 1.1);     // drifting inward
          var x = cx + Math.cos(v.a) * R * d * 2.2;
          var y = cy + Math.sin(v.a) * R * d * 2.2;
          for (var s = 0; s < v.spikes; s++) {
            var sa = (s / v.spikes) * TAU + t * .5;
            c.globalAlpha = .8; c.strokeStyle = v.col; c.lineWidth = 1.6;
            c.beginPath();
            c.moveTo(x + Math.cos(sa) * v.r, y + Math.sin(sa) * v.r);
            c.lineTo(x + Math.cos(sa) * v.r * 1.7, y + Math.sin(sa) * v.r * 1.7);
            c.stroke(); c.globalAlpha = 1;
          }
          disc(c, x, y, v.r, v.col, .95);
        });
      };
    },

    // an ant colony: trails between nests, traffic running both ways
    colony: function (w, h, rand) {
      var nodes = [], ants = [];
      for (var i = 0; i < 8; i++) nodes.push({ x: .08 + rand() * .84, y: .1 + rand() * .8, col: SPREAD[(i * 3) % SPREAD.length] });
      for (var j = 0; j < 80; j++) {
        var a = (rand() * nodes.length) | 0, b = (a + 1 + ((rand() * (nodes.length - 1)) | 0)) % nodes.length;
        ants.push({ a: a, b: b, t: rand(), sp: .07 + rand() * .12, col: rand() < .5 ? PAL.amber : PAL.gold });
      }
      return function (c, t, w, h) {
        ants.forEach(function (an) {
          var A = nodes[an.a], B = nodes[an.b];
          c.globalAlpha = .12; c.strokeStyle = PAL.lime; c.lineWidth = 1;
          c.beginPath(); c.moveTo(A.x * w, A.y * h); c.lineTo(B.x * w, B.y * h); c.stroke();
          c.globalAlpha = 1;
          var f = (an.t + t * an.sp) % 1;
          disc(c, (A.x + (B.x - A.x) * f) * w, (A.y + (B.y - A.y) * f) * h, 2.8, an.col, .95);
        });
        nodes.forEach(function (n) {
          glow(c, n.x * w, n.y * h, 34, n.col, .45);
          disc(c, n.x * w, n.y * h, 9, n.col, 1);
        });
      };
    },

    // cells dividing, their protective caps getting shorter each time
    telomere: function (w, h, rand) {
      var rows = 5, per = 7, cs = [];
      for (var r = 0; r < rows; r++) for (var i = 0; i < per; i++) {
        cs.push({ x: (i + .5) / per, y: (r + .5) / rows, ph: rand() * TAU,
                  col: SPREAD[(r * per + i) % SPREAD.length] });
      }
      return function (c, t, w, h) {
        var wear = ((t * .08) % 1);
        cs.forEach(function (p) {
          var x = p.x * w, y = p.y * h;
          var pulse = 1 + Math.sin(t * 1.2 + p.ph) * .06;
          ring(c, x, y, 15 * pulse, p.col, .75 - wear * .45, 2.2);
          disc(c, x, y, 4, p.col, .9 - wear * .5);
          // the cap, visibly shortening
          var capLen = (1 - wear) * 11;
          c.globalAlpha = .95; c.strokeStyle = wear > .7 ? PAL.coral : PAL.lime;
          c.lineWidth = 3; c.lineCap = 'round';
          c.beginPath(); c.moveTo(x - capLen, y - 19); c.lineTo(x + capLen, y - 19); c.stroke();
          c.globalAlpha = 1;
        });
      };
    },

    // every piece swapped out, and the shape still holding
    replace: function (w, h, rand) {
      var cols = 14, rows = 7, cells = [];
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        cells.push({ x: (x + .5) / cols, y: (y + .5) / rows, when: rand(),
                     col: SPREAD[(x * 3 + y) % SPREAD.length] });
      }
      return function (c, t, w, h) {
        var k = (t * .09) % 1;
        cells.forEach(function (p) {
          var d = Math.abs(p.when - k), flash = d < .05 ? (1 - d / .05) : 0;
          var x = p.x * w, y = p.y * h;
          if (p.when < k) {
            if (flash) glow(c, x, y, 16, p.col, flash * .6);
            disc(c, x, y, 5 + flash * 3, p.col, .9);
          } else {
            ring(c, x, y, 5, PAL.sky, .35, 1.4);
          }
        });
      };
    },

    /* --- earth and people ------------------------------------------ */

    // the ocean in layers: sunlit at the top, and below the light,
    // animals that have to make their own
    depths: function (w, h, rand) {
      var BANDS = [
        { to: .18, col: '#22D3EE' },   // sunlit
        { to: .40, col: '#2DD4BF' },   // twilight
        { to: .68, col: '#60A5FA' },   // dark
        { to: 1,   col: '#A78BFA' }    // the trenches
      ];
      var GLOW = ['#A3E635', '#F472B6', '#22D3EE', '#FBBF24', '#C084FC'];
      var life = [], snow = [];
      for (var i = 0; i < 64; i++) {
        var deep = rand();
        life.push({ x: rand(), y: deep, r: 3 + rand() * 9, ph: rand() * TAU,
                    sp: .008 + rand() * .026, lit: deep > .38,
                    col: deep > .38 ? GLOW[(rand() * GLOW.length) | 0] : '#0B1220' });
      }
      for (var j = 0; j < 40; j++) snow.push({ x: rand(), y: rand(), sp: .01 + rand() * .02 });
      return function (c, t, w, h) {
        var prev = 0;
        BANDS.forEach(function (b) {
          var g = c.createLinearGradient(0, prev * h, 0, b.to * h);
          g.addColorStop(0, b.col);
          g.addColorStop(1, 'rgba(0,0,0,0)');
          c.globalAlpha = .3; c.fillStyle = g;
          c.fillRect(0, prev * h, w, (b.to - prev) * h);
          c.globalAlpha = 1;
          // a visible rule where each zone ends
          c.globalAlpha = .5; c.strokeStyle = b.col; c.lineWidth = 1.2;
          c.beginPath(); c.moveTo(0, b.to * h); c.lineTo(w, b.to * h); c.stroke();
          c.globalAlpha = 1;
          prev = b.to;
        });
        // food drifting down out of the light
        snow.forEach(function (f) {
          disc(c, f.x * w, ((f.y + t * f.sp) % 1) * h, 1.6, '#FFFFFF', .3);
        });
        life.forEach(function (f) {
          var x = ((f.x + t * f.sp) % 1.12 - .06) * w;
          var y = (f.y + Math.sin(t * .5 + f.ph) * .018) * h;
          if (f.lit) {
            var beat = .55 + .45 * Math.sin(t * 1.8 + f.ph);
            glow(c, x, y, f.r * 5, f.col, .5 * beat);
            disc(c, x, y, f.r, f.col, .95);
          } else {
            // near the surface there is light from above, so they are shapes
            disc(c, x, y, f.r, '#0B1220', .5);
            ring(c, x, y, f.r, '#22D3EE', .45, 1.4);
          }
        });
      };
    },

    // a crowd where most of the figures are the people already gone
    crowd: function (w, h, rand) {
      var cols = 26, rows = 12, ppl = [];
      for (var y = 0; y < rows; y++) for (var x = 0; x < cols; x++) {
        ppl.push({ x: (x + .5) / cols, y: (y + .5) / rows, ph: rand() * TAU,
                   col: SPREAD[((x * 5 + y * 3) | 0) % SPREAD.length] });
      }
      // roughly one in fifteen of everyone who ever lived is alive now
      var ALIVE = 1 / 15;
      return function (c, t, w, h) {
        ppl.forEach(function (p, i) {
          var living = (i % 15) === 0;
          var x = p.x * w, y = p.y * h + Math.sin(t * .8 + p.ph) * 2;
          if (living) {
            glow(c, x, y, 11, p.col, .55);
            disc(c, x, y, 3.6, p.col, 1);
          } else {
            disc(c, x, y, 2.6, p.col, .22);
          }
        });
      };
    },

    // plants taking a city back, green climbing over grey
    overgrow: function (w, h, rand) {
      var GREENS = [PAL.lime, PAL.emerald, PAL.teal];
      var blocks = [], vines = [];
      for (var i = 0; i < 11; i++) {
        blocks.push({ x: rand(), wd: .05 + rand() * .07, ht: .2 + rand() * .5 });
      }
      for (var j = 0; j < 38; j++) {
        vines.push({ x: rand(), grow: rand(), sway: rand() * TAU,
                     col: GREENS[(rand() * 3) | 0], len: .2 + rand() * .5 });
      }
      return function (c, t, w, h) {
        blocks.forEach(function (b) {
          c.globalAlpha = .3; c.fillStyle = PAL.sky;
          c.fillRect(b.x * w, h - b.ht * h, b.wd * w, b.ht * h);
          c.globalAlpha = 1;
        });
        var k = (t * .07) % 1;
        vines.forEach(function (v) {
          var grown = Math.min(1, Math.max(0, k * 1.6 - v.grow * .6));
          if (grown <= 0) return;
          var x = v.x * w;
          c.globalAlpha = .85; c.strokeStyle = v.col; c.lineWidth = 2.2; c.lineCap = 'round';
          c.beginPath();
          for (var s = 0; s <= 14; s++) {
            var f = (s / 14) * grown * v.len;
            var px = x + Math.sin(f * 12 + v.sway) * 11;
            var py = h - f * h;
            s ? c.lineTo(px, py) : c.moveTo(px, py);
          }
          c.stroke(); c.globalAlpha = 1;
          var tipY = h - grown * v.len * h;
          disc(c, x + Math.sin(grown * v.len * 12 + v.sway) * 11, tipY, 3.4,
               grown > .8 ? PAL.magenta : v.col, .95);
        });
      };
    },

    // a night of sleep: the stages cycling, dreams in the deep end
    sleepcycle: function (w, h, rand) {
      var STAGE = [PAL.cyan, PAL.sky, PAL.violet, PAL.orchid, PAL.magenta];
      var motes = [];
      for (var i = 0; i < 26; i++) motes.push({ x: rand(), y: rand(), ph: rand() * TAU, col: SPREAD[(rand() * SPREAD.length) | 0] });
      return function (c, t, w, h) {
        // five stacked bands, one per stage, with a cursor running the night
        var bh = h / STAGE.length;
        STAGE.forEach(function (col, i) {
          c.globalAlpha = .13; c.fillStyle = col;
          c.fillRect(0, i * bh, w, bh); c.globalAlpha = 1;
        });
        c.lineWidth = 2.6; c.lineCap = 'round';
        c.beginPath();
        for (var x = 0; x <= w; x += 5) {
          var f = x / w;
          // four cycles a night, dipping deep then rising toward dreaming
          var depth = .5 + .42 * Math.sin(f * TAU * 4 - Math.PI / 2);
          var y = depth * h;
          x ? c.lineTo(x, y) : c.moveTo(x, y);
        }
        var g = c.createLinearGradient(0, 0, w, 0);
        g.addColorStop(0, PAL.cyan); g.addColorStop(.5, PAL.violet); g.addColorStop(1, PAL.magenta);
        c.strokeStyle = g; c.stroke();
        var cf = (t * .09) % 1;
        var cy = (.5 + .42 * Math.sin(cf * TAU * 4 - Math.PI / 2)) * h;
        glow(c, cf * w, cy, 22, PAL.gold, .6);
        disc(c, cf * w, cy, 6, PAL.gold, 1);
        motes.forEach(function (m) {
          disc(c, ((m.x + t * .01) % 1) * w, (m.y + Math.sin(t * .4 + m.ph) * .03) * h, 2, m.col, .35);
        });
      };
    },

    // attention wandering off the thing it is supposed to be on
    attention: function (w, h, rand) {
      var distractions = [];
      for (var i = 0; i < 14; i++) {
        distractions.push({ x: rand(), y: rand(), r: 4 + rand() * 8, ph: rand() * TAU,
                            col: SPREAD[(rand() * SPREAD.length) | 0] });
      }
      return function (c, t, w, h) {
        var cx = w * .5, cy = h * .5;
        ring(c, cx, cy, Math.min(w, h) * .17, PAL.cyan, .5, 2.5);
        distractions.forEach(function (d) {
          var pull = .5 + .5 * Math.sin(t * .5 + d.ph);
          var x = cx + (d.x - .5) * w * (.35 + pull * .6);
          var y = cy + (d.y - .5) * h * (.35 + pull * .6);
          glow(c, x, y, d.r * 3, d.col, .3 * pull);
          disc(c, x, y, d.r, d.col, .45 + pull * .5);
        });
        // the focus, which keeps sliding off centre
        var fx = cx + Math.sin(t * .43) * w * .19, fy = cy + Math.cos(t * .31) * h * .17;
        glow(c, fx, fy, 30, PAL.gold, .7);
        disc(c, fx, fy, 8, PAL.gold, 1);
      };
    },

    // a rhythm slowing down and finally stopping
    pulse: function (w, h, rand) {
      var motes = [];
      for (var i = 0; i < 22; i++) motes.push({ x: rand(), y: rand(), ph: rand() * TAU, col: SPREAD[(rand() * SPREAD.length) | 0] });
      return function (c, t, w, h) {
        var slow = (t * .06) % 1;                        // 0 lively, 1 stopped
        var rate = 2.4 * (1 - slow * .92);
        c.lineWidth = 3; c.lineCap = 'round'; c.lineJoin = 'round';
        c.beginPath();
        for (var x = 0; x <= w; x += 3) {
          var f = x / w;
          var beat = (f * 6 * (1 - slow * .7) + t * rate * .1) % 1;
          var spike = beat < .08 ? Math.sin(beat / .08 * Math.PI) : 0;
          var y = h * .5 - spike * h * .3 * (1 - slow);
          x ? c.lineTo(x, y) : c.moveTo(x, y);
        }
        var g = c.createLinearGradient(0, 0, w, 0);
        g.addColorStop(0, PAL.lime);
        g.addColorStop(.55, PAL.gold);
        g.addColorStop(1, PAL.coral);
        c.strokeStyle = g; c.globalAlpha = .95; c.stroke(); c.globalAlpha = 1;
        // as the rhythm fades the pieces drift free
        motes.forEach(function (m) {
          var drift = slow * .3;
          disc(c, ((m.x + t * .012) % 1) * w,
               (m.y + Math.sin(t * .5 + m.ph) * .04 + drift * (m.y - .5)) * h,
               2.6, m.col, .25 + .5 * (1 - slow));
        });
      };
    },

    // the same stretch of time, felt at two different speeds
    timewarp: function (w, h, rand) {
      var COL = [PAL.cyan, PAL.lime, PAL.amber, PAL.magenta, PAL.violet, PAL.teal];
      return function (c, t, w, h) {
        for (var row = 0; row < 2; row++) {
          var y = h * (row ? .68 : .32);
          var slowed = row === 1;
          var n = 15;
          for (var i = 0; i < n; i++) {
            var speed = slowed ? .18 : .5;
            var f = ((i / n) + t * speed) % 1;
            var r = slowed ? 7 : 4;
            var col = COL[i % COL.length];
            glow(c, f * w, y, r * 3, col, slowed ? .35 : .2);
            disc(c, f * w, y, r, col, slowed ? .95 : .6);
          }
          c.globalAlpha = .18; c.strokeStyle = PAL.white; c.lineWidth = 1;
          c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke(); c.globalAlpha = 1;
        }
      };
    }
  };

  /* ================= runner ======================================== */

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
      // a composed frame, not t=0, so reduced-motion still sees the idea
      if (REDUCED) { c.clearRect(0, 0, w, h); draw(c, 2.4, w, h); return; }
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
