# -*- coding: utf-8 -*-
"""All of Context's content. One dict per topic; build.py does the rest.

Each topic carries:
    slug     url + filename
    kicker   the small category label
    hue      blue | amber | coral | green | violet | teal
    title    the question, as a person would ask it
    teaser   one line for the card on the home page
    answer   the payoff, up front, before any explanation
    icon     small svg for the card
    svg      the figure
    controls the things you can operate
    js       what makes the figure move
    sections the explanation, in plain language
"""

TOPICS = [

# ---------------------------------------------------------------- 01
{
 'slug': 'time-speeds-up',
 'kicker': 'Your head',
 'hue': 'violet',
 'title': 'Why does a year feel faster every time?',
 'teaser': 'A summer lasted forever when you were eight. Now it is gone by June.',
 'answer': 'Your brain judges a year against everything you have already lived. '
           'At eight, one year is an eighth of your whole life. At forty it is a '
           'fortieth — the same year, a far smaller slice.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <circle cx="32" cy="32" r="22" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <path d="M32 18v15l10 6" fill="none" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 250" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Your life as a row of years, with this year highlighted</title>
  <text class="f-label" x="10" y="26">EVERY YEAR YOU HAVE LIVED</text>
  <g id="cells"></g>
  <text class="f-label" x="10" y="150">THIS YEAR, AS A SHARE OF YOUR LIFE</text>
  <rect x="10" y="164" width="640" height="26" rx="13" fill="#fff" stroke="var(--border)"/>
  <rect id="shareBar" x="10" y="164" width="0" height="26" rx="13" class="f-fill"/>
  <text class="f-value" id="shareTxt" x="10" y="222">&#8212;</text>
</svg>''',
 'controls': '''<div class="control">
  <label for="age">Your age</label>
  <input type="range" id="age" min="5" max="80" step="1" value="8">
  <span class="readout" id="ageOut">8</span>
</div>
<div class="control" style="flex:0 0 auto">
  <label>One year feels like</label>
  <span class="readout" id="feelOut">&#8212;</span>
</div>''',
 'js': '''
var age = document.getElementById('age'), cells = document.getElementById('cells');
var NS = 'http://www.w3.org/2000/svg';

function draw() {
  var n = +age.value;
  document.getElementById('ageOut').textContent = n;
  cells.textContent = '';
  var W = 640, gap = n > 45 ? 1 : 2, w = (W - gap * (n - 1)) / n;
  for (var i = 0; i < n; i++) {
    var r = document.createElementNS(NS, 'rect');
    r.setAttribute('x', 10 + i * (w + gap));
    r.setAttribute('y', 40);
    r.setAttribute('width', Math.max(w, 0.5));
    r.setAttribute('height', 62);
    r.setAttribute('rx', Math.min(3, w / 2));
    r.setAttribute('fill', i === n - 1 ? 'var(--bright)' : 'var(--wash)');
    r.setAttribute('stroke', i === n - 1 ? 'none' : 'var(--border)');
    cells.appendChild(r);
  }
  var share = 100 / n;
  document.getElementById('shareBar').setAttribute('width', Math.max(640 * share / 100, 3));
  document.getElementById('shareTxt').textContent = share.toFixed(1) + '% of your life so far';
  // how long a year at this age feels, measured against a year at age 8
  var months = 12 * (8 / n);
  document.getElementById('feelOut').textContent =
    n <= 8 ? '12 months' : months.toFixed(1) + ' months at age 8';
}
age.addEventListener('input', draw);
draw();
''',
 'caption': 'Drag your age. Each block is one year you have lived, and the coloured '
            'one is the year happening now. It does not get shorter — it just gets '
            'smaller next to everything else.',
 'sections': [
   {'h': 'Nothing is actually speeding up',
    'p': ['A year is the same length it has always been. What changes is what you '
          'are comparing it against.',
          'When you are eight, twelve months is a <strong>huge fraction</strong> of '
          'everything you can remember. At forty, the same twelve months lands on '
          'top of a much bigger pile, so it takes up less room.']},
   {'h': 'The other half is novelty',
    'p': ['Your memory stores new things and skips repeats. A first summer at a new '
          'school is dense with firsts, so it leaves a thick trace and feels long '
          'when you look back.',
          'A year of the same commute compresses into almost nothing, because there '
          'was little worth filing separately.']},
   {'h': 'What actually slows it down', 'tips': [
     'Do things you have never done before — new places make thick memories.',
     'Break routine deliberately, even in small ways: a different route, a different room.',
     'Write things down. A year you can recall in detail is a year that felt long.']},
 ],
},

# ---------------------------------------------------------------- 02
{
 'slug': 'onion-tears',
 'kicker': 'Kitchen',
 'hue': 'green',
 'title': 'Why do onions make you cry?',
 'teaser': 'And which of the kitchen tricks actually do something.',
 'answer': 'Cutting an onion breaks cells that mix two harmless chemicals into a gas. '
           'The gas floats up, meets the water in your eyes, and turns into a mild '
           'acid. Your eyes water to wash it out.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <path d="M32 22c10 0 17 9 17 18 0 9-8 15-17 15s-17-6-17-15c0-9 7-18 17-18z" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <path d="M32 22c-2-6-7-9-13-9 1 6 5 9 13 9" fill="none" stroke="var(--bright)" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M24 32c-3 6-3 14 0 19M40 32c3 6 3 14 0 19" fill="none" stroke="var(--bright)" stroke-width="2" opacity=".5"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">An onion releasing gas, and how much your eyes sting</title>
  <g id="gas"></g>
  <path d="M180 150c26 0 46 22 46 50s-20 50-46 50-46-22-46-50 20-50 46-50z" class="f-soft" stroke="var(--bright)" stroke-width="2.5"/>
  <path d="M180 150v100M156 160c-8 16-8 44 0 66M204 160c8 16 8 44 0 66" fill="none" stroke="var(--bright)" stroke-width="2" opacity=".5"/>
  <text class="f-label" x="360" y="120">HOW MUCH IT STINGS</text>
  <rect x="360" y="136" width="280" height="30" rx="15" fill="#fff" stroke="var(--border)"/>
  <rect id="stingBar" x="360" y="136" width="280" height="30" rx="15" class="f-fill"/>
  <text class="f-value" id="stingTxt" x="360" y="196">100</text>
</svg>''',
 'controls': '''<div class="chips" role="group" aria-label="Things you can try">
  <button class="chip" id="mChill" aria-pressed="false">Chill it first</button>
  <button class="chip" id="mSharp" aria-pressed="false">Sharp knife</button>
  <button class="chip" id="mRoot" aria-pressed="false">Leave the root on</button>
  <button class="chip" id="mFan" aria-pressed="false">Fan or open window</button>
  <button class="chip" id="mBread" aria-pressed="false">Bread in your mouth</button>
</div>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
// how much each trick actually cuts the gas reaching your eyes
var TRICKS = [
  ['mChill', 35], ['mSharp', 25], ['mRoot', 12], ['mFan', 22], ['mBread', 0]
];
var gas = document.getElementById('gas'), puffs = [];
for (var i = 0; i < 26; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('r', 3 + Math.random() * 4);
  c.setAttribute('fill', 'var(--bright)');
  c.dataset.x = 140 + Math.random() * 80;
  c.dataset.t = Math.random();
  gas.appendChild(c);
  puffs.push(c);
}

function level() {
  var v = 100;
  TRICKS.forEach(function (t) {
    if (document.getElementById(t[0]).getAttribute('aria-pressed') === 'true') v -= t[1];
  });
  return Math.max(v, 6);
}

function paint() {
  var v = level();
  document.getElementById('stingBar').setAttribute('width', 280 * v / 100);
  document.getElementById('stingTxt').textContent =
    v > 80 ? 'Streaming' : v > 55 ? 'Watering' : v > 30 ? 'Just a prickle' : 'Barely anything';
  puffs.forEach(function (p) { p.style.opacity = (v / 100) * 0.75; });
}

TRICKS.forEach(function (t) {
  var b = document.getElementById(t[0]);
  b.addEventListener('click', function () {
    b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    paint();
  });
});

var t0 = null;
function tick(ts) {
  if (t0 === null) t0 = ts;
  var dt = (ts - t0) / 1000;
  puffs.forEach(function (p) {
    var f = ((+p.dataset.t) + dt * 0.16) % 1;
    p.setAttribute('cx', (+p.dataset.x) + Math.sin(f * 7) * 14);
    p.setAttribute('cy', 250 - f * 210);
  });
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
paint();
''',
 'caption': 'Switch the tricks on and off. Chilling the onion and using a sharp knife '
            'do most of the work. The bread trick is in there because everyone '
            'suggests it — it changes nothing.',
 'sections': [
   {'h': 'What is actually in the air',
    'p': ['An onion keeps two ingredients in separate compartments: a sulphur compound '
          'and an enzyme. Whole, they never meet. Cutting smashes those compartments '
          'together and the reaction makes a light, floaty gas.',
          'That gas drifts up to the nearest wet surface, which is usually your eyes. '
          'There it becomes a weak acid, and your eyes flush it out with tears. '
          '<strong>Nothing is being damaged</strong> — this is the rinse cycle working.']},
   {'h': 'Why the good tricks work',
    'p': ['Every trick that helps does one of two things: slow the reaction down, or '
          'move the gas away from your face.',
          'Cold slows chemistry, so half an hour in the fridge genuinely helps. A sharp '
          'blade slices cells instead of crushing them, so less gets mixed. A fan or an '
          'open window carries the gas off before it reaches you.']},
   {'h': 'The short version', 'tips': [
     'Chill the onion for 30 minutes before you start.',
     'Use the sharpest knife you own — a blunt one crushes and makes it worse.',
     'Cut near a window or an extractor fan.',
     'Skip the bread, the spoon and the candle. They do nothing.']},
 ],
},

# ---------------------------------------------------------------- 03
{
 'slug': 'bigger-box',
 'kicker': 'Money',
 'hue': 'amber',
 'title': 'Is the big box actually cheaper?',
 'teaser': 'Usually. Not always — and the shop is counting on you not checking.',
 'answer': 'Compare the price per 100 grams, not the price on the front. Big packs are '
           'normally better value, but often enough the small one wins, and the label '
           'never tells you which is which.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <rect x="10" y="30" width="18" height="20" rx="3" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <rect x="34" y="18" width="22" height="32" rx="3" fill="none" stroke="var(--bright)" stroke-width="3"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Two pack sizes compared by price per 100 grams</title>
  <rect id="boxA" x="80" y="150" width="110" height="90" rx="10" class="f-soft" stroke="var(--bright)" stroke-width="2.5"/>
  <text class="f-label" x="135" y="264" text-anchor="middle">SMALL &#183; 250 g</text>
  <text class="f-value" id="perA" x="135" y="134" text-anchor="middle">&#8212;</text>
  <rect id="boxB" x="400" y="60" width="180" height="180" rx="10" class="f-soft" stroke="var(--bright)" stroke-width="2.5"/>
  <text class="f-label" x="490" y="264" text-anchor="middle">BIG &#183; 750 g</text>
  <text class="f-value" id="perB" x="490" y="44" text-anchor="middle">&#8212;</text>
  <g id="winner" opacity="0">
    <rect id="winBox" x="0" y="0" width="150" height="30" rx="15" class="f-fill"/>
    <text id="winTxt" x="0" y="0" text-anchor="middle" fill="#fff"
          style="font-family:var(--display);font-size:14px;font-weight:700">BETTER VALUE</text>
  </g>
</svg>''',
 'controls': '''<div class="control">
  <label for="pa">Small pack</label>
  <input type="range" id="pa" min="50" max="400" step="5" value="180">
  <span class="readout" id="paOut">&#8212;</span>
</div>
<div class="control">
  <label for="pb">Big pack</label>
  <input type="range" id="pb" min="150" max="900" step="5" value="480">
  <span class="readout" id="pbOut">&#8212;</span>
</div>''',
 'js': '''
var pa = document.getElementById('pa'), pb = document.getElementById('pb');
var SIZE_A = 250, SIZE_B = 750;

function money(cents) { return '\\u00a3' + (cents / 100).toFixed(2); }

function draw() {
  var a = +pa.value, b = +pb.value;
  document.getElementById('paOut').textContent = money(a);
  document.getElementById('pbOut').textContent = money(b);

  var perA = a / (SIZE_A / 100), perB = b / (SIZE_B / 100);
  document.getElementById('perA').textContent = money(perA) + ' / 100g';
  document.getElementById('perB').textContent = money(perB) + ' / 100g';

  var aWins = perA < perB;
  var g = document.getElementById('winner');
  g.setAttribute('opacity', '1');
  var cx = aWins ? 135 : 490;
  document.getElementById('winBox').setAttribute('x', cx - 75);
  document.getElementById('winBox').setAttribute('y', aWins ? 160 : 120);
  document.getElementById('winTxt').setAttribute('x', cx);
  document.getElementById('winTxt').setAttribute('y', (aWins ? 160 : 120) + 20);
  var gap = Math.abs(perA - perB) / Math.max(perA, perB) * 100;
  document.getElementById('winTxt').textContent =
    gap < 1 ? 'LINE BALL' : 'BETTER BY ' + gap.toFixed(0) + '%';
}
pa.addEventListener('input', draw);
pb.addEventListener('input', draw);
draw();
''',
 'caption': 'Slide the two prices around. The badge follows whichever pack is actually '
            'cheaper per 100 g — which is not always the big one, however much bigger '
            'it looks.',
 'sections': [
   {'h': 'The number on the front is the wrong number',
    'p': ['A price tag answers "what leaves my wallet today". It cannot answer "is this '
          'good value", because it says nothing about how much you are getting.',
          'The only figure that compares two packs is <strong>price divided by size</strong>. '
          'Most shops print it in small grey type on the shelf label. It is the single '
          'most useful number in the shop and the least legible.']},
   {'h': 'Why bigger is usually, but not always, cheaper',
    'p': ['Packing, shipping and shelf space cost roughly the same whether a box is big '
          'or small, so spreading them over more product usually lowers the unit price.',
          'But pricing is also a guess about what you will pay. Family sizes get promoted, '
          'then quietly stop being a bargain once the promotion ends. Small packs on offer '
          'routinely beat big packs at full price.']},
   {'h': 'In the aisle', 'tips': [
     'Read the small per-unit price on the shelf label, not the big one on the pack.',
     'Check that both labels use the same unit — per 100 g against per kg is a trap.',
     'Bigger is only cheaper if you actually use it before it goes off.']},
 ],
},

# ---------------------------------------------------------------- 04
{
 'slug': 'cold-phone',
 'kicker': 'Tech',
 'hue': 'blue',
 'title': 'Why does your phone die in the cold?',
 'teaser': 'It jumps from 40% to nothing — then recovers indoors.',
 'answer': 'Cold slows the chemistry inside the battery, so it cannot push charge out '
           'fast enough. The energy is still in there. The battery just cannot hand it '
           'over until it warms up.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <rect x="12" y="20" width="34" height="24" rx="5" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <rect x="48" y="28" width="5" height="8" rx="2" fill="var(--bright)"/>
  <rect x="17" y="25" width="10" height="14" rx="2" fill="var(--bright)"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 280" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Usable battery charge against temperature</title>
  <rect x="60" y="90" width="230" height="110" rx="16" fill="#fff" stroke="var(--bright)" stroke-width="3"/>
  <rect x="292" y="126" width="14" height="38" rx="5" class="f-fill"/>
  <rect id="fill" x="70" y="100" width="210" height="90" rx="9" class="f-fill"/>
  <text class="f-value" id="pctTxt" x="175" y="240" text-anchor="middle">100%</text>
  <text class="f-label" x="175" y="70" text-anchor="middle">WHAT YOU CAN ACTUALLY USE</text>
  <text class="f-label" x="400" y="70">WHAT THE PHONE REPORTS</text>
  <text class="f-value" id="showTxt" x="400" y="112" style="font-size:34px">100%</text>
  <text class="f-label" id="noteTxt" x="400" y="150">Everything is fine.</text>
  <rect x="400" y="180" width="200" height="12" rx="6" fill="#fff" stroke="var(--border)"/>
  <rect id="tempBar" x="400" y="180" width="140" height="12" rx="6" class="f-fill"/>
  <text class="f-label" x="400" y="216">COLD</text>
  <text class="f-label" x="600" y="216" text-anchor="end">WARM</text>
</svg>''',
 'controls': '''<div class="control">
  <label for="temp">Temperature</label>
  <input type="range" id="temp" min="-20" max="35" step="1" value="22">
  <span class="readout" id="tempOut">22&#176;C</span>
</div>''',
 'js': '''
var temp = document.getElementById('temp');

function draw() {
  var t = +temp.value;
  document.getElementById('tempOut').textContent = t + '\\u00b0C';
  // usable capacity falls away steeply below freezing, flat once warm
  var cap = t >= 20 ? 100 : 100 - Math.pow((20 - t) / 40, 1.5) * 105;
  cap = Math.max(18, Math.min(100, cap));

  document.getElementById('fill').setAttribute('width', 210 * cap / 100);
  document.getElementById('pctTxt').textContent = Math.round(cap) + '% available';
  document.getElementById('showTxt').textContent = t < 5 ? 'jumps around' : Math.round(cap) + '%';
  document.getElementById('noteTxt').textContent =
    t < -5 ? 'It may shut off with charge left.'
    : t < 5 ? 'The reading gets unreliable.'
    : t < 15 ? 'Slightly short, nothing odd.'
    : 'Everything is fine.';
  document.getElementById('tempBar').setAttribute('width', 200 * (t + 20) / 55);
}
temp.addEventListener('input', draw);
draw();
''',
 'caption': 'Drag the temperature down. The charge does not leave the battery — the '
            'amount it can deliver shrinks, and the phone, which guesses the percentage '
            'from voltage, starts reporting nonsense.',
 'sections': [
   {'h': 'The charge is still there',
    'p': ['A battery makes power by shuffling lithium ions through a liquid. Cool that '
          'liquid and everything moves more slowly, so the battery cannot supply current '
          'as quickly.',
          'Ask for a lot at once — camera, torch, mobile signal hunting — and the voltage '
          'sags. Your phone reads that sag as "empty" and shuts down, <strong>with charge '
          'still in the battery</strong>. Warm it up and the charge comes back.']},
   {'h': 'Why the percentage lies',
    'p': ['No phone measures charge directly. It measures voltage and infers the rest from '
          'a model built at room temperature.',
          'In the cold that model is simply wrong, which is why you get 40%, then 12%, then '
          'nothing, then 25% once you are indoors again.']},
   {'h': 'What to do in winter', 'tips': [
     'Keep the phone in an inside pocket — body heat is enough.',
     'If it shuts down cold, warm it in your hands before deciding it is broken.',
     'Do not charge a phone that is properly cold; let it reach room temperature first.']},
 ],
},

# ---------------------------------------------------------------- 05
{
 'slug': 'stale-bread',
 'kicker': 'Kitchen',
 'hue': 'amber',
 'title': 'Why is the fridge the worst place for bread?',
 'teaser': 'Stale is not the same thing as dry — which is why chilling backfires.',
 'answer': 'Going stale is starch quietly recrystallising, and that happens fastest just '
           'above freezing. The fridge sits exactly in the worst zone. The counter is '
           'slower; the freezer nearly stops it.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <path d="M14 30c0-8 8-12 18-12s18 4 18 12v14a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4z" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <path d="M22 30h20" stroke="var(--bright)" stroke-width="2.5" opacity=".55" stroke-linecap="round"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 290" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How quickly bread goes stale in different places</title>
  <path d="M70 90c0-30 30-44 68-44s68 14 68 44v78a12 12 0 0 1-12 12H82a12 12 0 0 1-12-12z"
        id="loaf" class="f-soft" stroke="var(--bright)" stroke-width="2.5"/>
  <g id="crystals"></g>
  <text class="f-label" x="330" y="70">HOW STALE IT IS</text>
  <rect x="330" y="86" width="300" height="30" rx="15" fill="#fff" stroke="var(--border)"/>
  <rect id="staleBar" x="330" y="86" width="0" height="30" rx="15" class="f-fill"/>
  <text class="f-value" id="staleTxt" x="330" y="146">Fresh</text>
  <text class="f-label" x="330" y="196">SAME BREAD, LEFT ON THE COUNTER</text>
  <rect x="330" y="212" width="300" height="14" rx="7" fill="#fff" stroke="var(--border)"/>
  <rect id="refBar" x="330" y="212" width="0" height="14" rx="7" fill="var(--border)"/>
</svg>''',
 'controls': '''<div class="chips" role="group" aria-label="Where you keep it">
  <button class="chip" id="wCounter" aria-pressed="true">Counter</button>
  <button class="chip" id="wFridge" aria-pressed="false">Fridge</button>
  <button class="chip" id="wFreezer" aria-pressed="false">Freezer</button>
</div>
<div class="control">
  <label for="days">Days</label>
  <input type="range" id="days" min="0" max="7" step="0.5" value="2">
  <span class="readout" id="daysOut">2</span>
</div>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
var RATE = { wCounter: 12, wFridge: 26, wFreezer: 1.5 };
var where = 'wCounter';
var days = document.getElementById('days');

var crystals = document.getElementById('crystals'), dots = [];
for (var i = 0; i < 40; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 86 + Math.random() * 104);
  c.setAttribute('cy', 66 + Math.random() * 106);
  c.setAttribute('r', 1.6 + Math.random() * 2.2);
  c.setAttribute('fill', 'var(--bright)');
  c.setAttribute('opacity', '0');
  crystals.appendChild(c);
  dots.push(c);
}

function draw() {
  var d = +days.value;
  document.getElementById('daysOut').textContent = d;
  var v = Math.min(100, d * RATE[where]);
  var ref = Math.min(100, d * RATE.wCounter);

  document.getElementById('staleBar').setAttribute('width', 300 * v / 100);
  document.getElementById('refBar').setAttribute('width', 300 * ref / 100);
  document.getElementById('staleTxt').textContent =
    v < 12 ? 'Fresh' : v < 35 ? 'Softening off' : v < 65 ? 'Firm and dull' : 'Toast it, honestly';
  dots.forEach(function (dot, i) {
    dot.setAttribute('opacity', i / dots.length < v / 100 ? 0.85 : 0);
  });
}

Object.keys(RATE).forEach(function (id) {
  document.getElementById(id).addEventListener('click', function () {
    where = id;
    Object.keys(RATE).forEach(function (o) {
      document.getElementById(o).setAttribute('aria-pressed', o === id ? 'true' : 'false');
    });
    draw();
  });
});
days.addEventListener('input', draw);
draw();
''',
 'caption': 'The grey bar underneath is always the counter, for comparison. Put the same '
            'loaf in the fridge and it stales roughly twice as fast — the freezer is the '
            'only place that really stops it.',
 'sections': [
   {'h': 'Stale is not dry',
    'p': ['It is easy to assume bread goes hard because it dries out. Wrap a loaf in a '
          'sealed bag so it cannot lose any water and it still goes stale.',
          'What is happening is that starch, forced into a loose disordered arrangement by '
          'baking, slowly settles back into ordered crystals. Those crystals grab water and '
          'stiffen the crumb. The bread is not drier — it is <strong>firmer, and holding '
          'its water differently</strong>.']},
   {'h': 'Why the fridge is the trap',
    'p': ['That recrystallising happens fastest a little above freezing — right where your '
          'fridge lives. Chilling bread makes it stale faster than leaving it out.',
          'Below freezing the molecules barely move, so a freezer nearly stops the clock. '
          'This is also why warming a stale slice revives it: heat breaks the crystals up '
          'again, for a while.']},
   {'h': 'Where to actually put it', 'tips': [
     'Eating it in a couple of days: counter, in a paper bag or a bread bin.',
     'Longer than that: slice it and freeze it, then toast straight from frozen.',
     'The fridge is for sandwiches, not for loaves.',
     'A stale slice in a warm oven for a few minutes comes back to life.']},
 ],
},

# ---------------------------------------------------------------- 06
{
 'slug': 'small-savings',
 'kicker': 'Money',
 'hue': 'green',
 'title': 'How does a little money turn into a lot?',
 'teaser': 'The part that does the work is the years, not the amount.',
 'answer': 'Money you put away earns a little. Then that little earns too. For years it '
           'looks like nothing is happening — the gap only opens up late, and then it '
           'opens fast.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <path d="M12 46c10 0 12-4 18-14s10-16 22-20" fill="none" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
  <circle cx="52" cy="12" r="4" fill="var(--bright)"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What you put in against what it grows to</title>
  <line class="f-faint" x1="60" y1="240" x2="640" y2="240"/>
  <!-- area first: it would otherwise paint over the deposits line -->
  <path id="totArea" d="" class="f-soft"/>
  <path id="inLine" d="" fill="none" stroke="var(--muted)" stroke-width="3" stroke-dasharray="7 5"/>
  <path id="totLine" d="" class="f-line"/>
  <text class="f-label" x="60" y="264">START</text>
  <text class="f-label" id="endLbl" x="640" y="264" text-anchor="end">40 YEARS</text>
  <text class="f-label" x="60" y="30">WHAT IT BECOMES</text>
  <text class="f-value" id="totTxt" x="60" y="58" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="330" y="30">YOU ACTUALLY PUT IN</text>
  <text class="f-value" id="inTxt" x="330" y="58" style="font-size:26px;fill:var(--muted)">&#8212;</text>
</svg>''',
 'controls': '''<div class="control">
  <label for="amt">Each month</label>
  <input type="range" id="amt" min="10" max="400" step="10" value="50">
  <span class="readout" id="amtOut">&#8212;</span>
</div>
<div class="control">
  <label for="yrs">For</label>
  <input type="range" id="yrs" min="1" max="40" step="1" value="30">
  <span class="readout" id="yrsOut">30 years</span>
</div>''',
 'js': '''
var amt = document.getElementById('amt'), yrs = document.getElementById('yrs');
var RATE = 0.06 / 12;   // 6% a year, a long-run average

function money(v) {
  return '\\u00a3' + Math.round(v).toLocaleString('en-GB');
}

function draw() {
  var m = +amt.value, y = +yrs.value;
  document.getElementById('amtOut').textContent = money(m);
  document.getElementById('yrsOut').textContent = y + (y === 1 ? ' year' : ' years');
  document.getElementById('endLbl').textContent = y + (y === 1 ? ' YEAR' : ' YEARS');

  var months = y * 12;
  var total = m * ((Math.pow(1 + RATE, months) - 1) / RATE);
  var paid = m * months;
  document.getElementById('totTxt').textContent = money(total);
  document.getElementById('inTxt').textContent = money(paid);

  var top = total;
  var tot = [], inp = [];
  for (var i = 0; i <= 60; i++) {
    var k = i / 60, mm = months * k;
    var t = m * ((Math.pow(1 + RATE, mm) - 1) / RATE);
    var p = m * mm;
    var x = 60 + 580 * k;
    tot.push([x, 240 - 200 * (t / top)]);
    inp.push([x, 240 - 200 * (p / top)]);
  }
  var d = function (pts) { return pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' '); };
  document.getElementById('totLine').setAttribute('d', d(tot));
  document.getElementById('inLine').setAttribute('d', d(inp));
  document.getElementById('totArea').setAttribute('d', d(tot) + ' L640 240 L60 240 Z');
}
amt.addEventListener('input', draw);
yrs.addEventListener('input', draw);
draw();
''',
 'caption': 'The dashed line is your own money going in, steadily. The coloured one is what '
            'it turns into. Drag the years down to ten and the two lines almost touch — '
            'nearly all of the gap arrives in the last stretch.',
 'sections': [
   {'h': 'Why it looks like nothing for so long',
    'p': ['In year one, your savings earn a small amount. In year two, your savings and '
          'that small amount both earn. The extra bit is tiny, so early on the whole thing '
          'looks like a slightly better piggy bank.',
          'But the growing part keeps growing, and it grows <strong>on itself</strong>. '
          'Halfway along, the interest starts earning more each year than you are putting '
          'in, and the line bends away from the dashed one.']},
   {'h': 'This is also how debt works',
    'p': ['Exactly the same machinery runs behind a credit card, only pointed at you. '
          'Unpaid interest joins the balance and then earns interest of its own.',
          'That is why a card balance you only make minimum payments on can take decades to '
          'clear, and why clearing expensive debt beats saving almost every time.']},
   {'h': 'What matters most', 'tips': [
     'Starting earlier beats saving more. Ten extra years usually outweighs doubling the amount.',
     'Make it automatic on payday so it never becomes a decision.',
     'Pay off anything charging more than your savings earn, first.']},
 ],
},

# ---------------------------------------------------------------- 07
{
 'slug': 'shower-curtain',
 'kicker': 'Home',
 'hue': 'teal',
 'title': 'Why does the shower curtain attack you?',
 'teaser': 'Every single time, it reaches in and sticks to your leg.',
 'answer': 'Falling water drags air down with it and flings it outward, thinning the air '
           'just inside the curtain. The ordinary air in the bathroom then pushes the '
           'curtain in. Nothing is pulling it.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <path d="M12 13h20" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
  <rect x="15" y="15" width="14" height="6" rx="3" fill="var(--bright)"/>
  <path d="M18 27v7M22 25v9M26 27v7" stroke="var(--bright)" stroke-width="2.5" stroke-linecap="round" opacity=".55"/>
  <path d="M46 11c-7 13 6 20 0 41" fill="none" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 320" role="img" aria-labelledby="figTitle">
  <title id="figTitle">A shower curtain bowing inward while the water runs</title>
  <rect x="120" y="34" width="300" height="8" rx="4" fill="var(--border)"/>
  <path d="M150 44h70v14h-70z" class="f-fill"/>
  <g id="water"></g>
  <path id="curtain" d="M400 44 C400 150 400 190 400 296" fill="none" stroke="var(--bright)" stroke-width="5" stroke-linecap="round"/>
  <g id="arrows" opacity="0">
    <path d="M520 150 L440 150" stroke="var(--bright)" stroke-width="3" marker-end="url(#ah)"/>
    <path d="M520 200 L440 200" stroke="var(--bright)" stroke-width="3" marker-end="url(#ah)"/>
    <text class="f-label" x="530" y="155">ROOM AIR</text>
    <text class="f-label" x="530" y="205">PUSHES IN</text>
  </g>
  <defs>
    <marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">
      <path d="M0 0 L9 4.5 L0 9 z" fill="var(--bright)"/>
    </marker>
  </defs>
  <text class="f-label" x="120" y="300">INSIDE</text>
  <text class="f-value" id="pressTxt" x="120" y="272">&#8212;</text>
</svg>''',
 'controls': '''<div class="switch" role="group" aria-label="Water">
  <button id="wOff" aria-pressed="true">Water off</button>
  <button id="wOn" aria-pressed="false">Water on</button>
</div>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
var on = false, bow = 0;
var water = document.getElementById('water'), drops = [];
for (var i = 0; i < 30; i++) {
  var l = document.createElementNS(NS, 'line');
  l.setAttribute('stroke', 'var(--bright)');
  l.setAttribute('stroke-width', '2');
  l.setAttribute('stroke-linecap', 'round');
  l.setAttribute('opacity', '0');
  l.dataset.x = 156 + Math.random() * 58;
  l.dataset.t = Math.random();
  water.appendChild(l);
  drops.push(l);
}

function setMode(v) {
  on = v;
  document.getElementById('wOn').setAttribute('aria-pressed', v ? 'true' : 'false');
  document.getElementById('wOff').setAttribute('aria-pressed', v ? 'false' : 'true');
  document.getElementById('arrows').setAttribute('opacity', v ? '1' : '0');
  document.getElementById('pressTxt').textContent = v ? 'Air pressure: lower' : 'Air pressure: even';
}
document.getElementById('wOn').addEventListener('click', function () { setMode(true); });
document.getElementById('wOff').addEventListener('click', function () { setMode(false); });

var t0 = null;
function tick(ts) {
  if (t0 === null) t0 = ts;
  var dt = (ts - t0) / 1000;
  bow += ((on ? 58 : 0) - bow) * 0.06;
  document.getElementById('curtain').setAttribute('d',
    'M400 44 C' + (400 - bow) + ' 150 ' + (400 - bow) + ' 190 400 296');
  drops.forEach(function (l) {
    if (!on) { l.setAttribute('opacity', '0'); return; }
    var f = ((+l.dataset.t) + dt * 0.9) % 1;
    var x = +l.dataset.x;
    l.setAttribute('x1', x); l.setAttribute('x2', x + 3);
    l.setAttribute('y1', 58 + f * 230); l.setAttribute('y2', 58 + f * 230 + 14);
    l.setAttribute('opacity', '0.75');
  });
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
setMode(false);
''',
 'caption': 'Turn the water on. The curtain moves because the air inside got thinner, not '
            'because the water grabbed it — which is why it happens with cold water too.',
 'sections': [
   {'h': 'Moving air is thinner air',
    'p': ['A shower is thousands of drops falling fast, and each one drags a little air '
          'along with it. All that air has to go somewhere, so it spills outward near the '
          'floor and circles around.',
          'Air that is moving quickly presses on its surroundings a little <strong>less</strong> '
          'than still air does. So the inside of the curtain is pressed slightly less hard '
          'than the outside, and the difference — small, but spread over a big sheet — '
          'pushes it inward.']},
   {'h': 'Why hot water is not the answer',
    'p': ['Warm air rising does add to the effect, and a hot shower usually pulls the '
          'curtain harder. But run the shower cold and the curtain still comes in.',
          'That is the giveaway: if heat were the cause, cold water would leave the curtain '
          'alone. The moving air is doing most of the work.']},
   {'h': 'Making it stop', 'tips': [
     'Weight the bottom hem — clips, magnets, or a curtain with a weighted edge.',
     'Use a longer curtain and let it sit inside the tub, so there is less loose sheet.',
     'A curved rail moves the whole thing further from your legs.']},
 ],
},

# ---------------------------------------------------------------- 08
{
 'slug': 'contagious-yawns',
 'kicker': 'Your head',
 'hue': 'violet',
 'title': 'Why are yawns contagious?',
 'teaser': 'There is a decent chance you have already done one reading this.',
 'answer': 'Watching someone yawn quietly switches on the same parts of your brain that '
           'would produce a yawn of your own. It is the same copying reflex that makes '
           'laughter spread — and it works better on people you like.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <circle cx="32" cy="32" r="21" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <ellipse cx="32" cy="40" rx="7" ry="9" fill="var(--bright)"/>
  <path d="M22 24h6M36 24h6" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 260" role="img" aria-labelledby="figTitle">
  <title id="figTitle">A room of faces catching each other's yawns</title>
  <g id="faces"></g>
  <text class="f-label" x="10" y="248">CLICK ANY FACE TO START A YAWN</text>
  <text class="f-value" id="caughtTxt" x="650" y="248" text-anchor="end">0 of 12 caught it</text>
</svg>''',
 'controls': '''<div class="control">
  <label for="close">How close are they</label>
  <input type="range" id="close" min="0" max="100" step="1" value="60">
  <span class="readout" id="closeOut">Friends</span>
</div>
<button class="btn" id="reset">Start over</button>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
var faces = document.getElementById('faces'), close = document.getElementById('close');
var N = 12, state = [], nodes = [];

for (var i = 0; i < N; i++) {
  var col = i % 6, row = (i / 6) | 0;
  var cx = 70 + col * 105, cy = 70 + row * 100;
  var g = document.createElementNS(NS, 'g');
  g.setAttribute('style', 'cursor:pointer');
  g.innerHTML =
    '<circle cx="' + cx + '" cy="' + cy + '" r="34" fill="#fff" stroke="var(--border)" stroke-width="2.5"/>' +
    '<circle cx="' + (cx - 11) + '" cy="' + (cy - 9) + '" r="3.2" fill="var(--muted)"/>' +
    '<circle cx="' + (cx + 11) + '" cy="' + (cy - 9) + '" r="3.2" fill="var(--muted)"/>' +
    '<ellipse cx="' + cx + '" cy="' + (cy + 12) + '" rx="6" ry="3" fill="var(--muted)"/>';
  faces.appendChild(g);
  nodes.push({ g: g, cx: cx, cy: cy, circle: g.children[0], mouth: g.children[3] });
  state.push(0);
  (function (k) { g.addEventListener('click', function () { infect(k); }); }(i));
}

function paint() {
  nodes.forEach(function (n, i) {
    var yawning = state[i] > 0;
    n.circle.setAttribute('fill', yawning ? 'var(--wash)' : '#fff');
    n.circle.setAttribute('stroke', yawning ? 'var(--bright)' : 'var(--border)');
    n.mouth.setAttribute('ry', yawning ? 13 : 3);
    n.mouth.setAttribute('rx', yawning ? 8 : 6);
    n.mouth.setAttribute('fill', yawning ? 'var(--bright)' : 'var(--muted)');
  });
  var c = state.filter(function (s) { return s > 0; }).length;
  document.getElementById('caughtTxt').textContent = c + ' of ' + N + ' caught it';
}

function infect(i) {
  if (state[i] > 0) return;
  state[i] = 1;
  paint();
  // closeness raises the chance a neighbour catches it
  var p = 0.15 + (+close.value / 100) * 0.75;
  nodes.forEach(function (n, j) {
    if (state[j] > 0) return;
    var d = Math.hypot(n.cx - nodes[i].cx, n.cy - nodes[i].cy);
    if (d > 160) return;
    if (Math.random() < p) setTimeout(function () { infect(j); }, 500 + Math.random() * 900);
  });
}

close.addEventListener('input', function () {
  var v = +close.value;
  document.getElementById('closeOut').textContent =
    v < 25 ? 'Strangers' : v < 55 ? 'Colleagues' : v < 80 ? 'Friends' : 'Family';
});

document.getElementById('reset').addEventListener('click', function () {
  state = state.map(function () { return 0; });
  paint();
});
paint();
''',
 'caption': 'Click a face and watch it travel. Slide the closeness down to strangers and '
            'it mostly dies out — the effect really is stronger between people who know '
            'each other.',
 'sections': [
   {'h': 'Your brain rehearses what it watches',
    'p': ['A lot of what you see other people do gets quietly run through your own motor '
          'system, as if you were about to do it too. Most of the time that rehearsal stops '
          'before it becomes movement.',
          'Yawning slips through. Watching one, hearing one, even reading the word is often '
          'enough to tip the rehearsal into <strong>the real thing</strong>.']},
   {'h': 'It tracks who you care about',
    'p': ['Contagious yawning is strongest with family, weaker with friends, weaker still '
          'with strangers. It travels between dogs and their owners, and across a few other '
          'social species.',
          'Children mostly do not catch yawns until around age four or five, which is roughly '
          'when a lot of other social copying arrives.']},
   {'h': 'And the yawn itself?',
    'p': ['The old story was that yawning tops up oxygen. That one has not held up — '
          'breathing extra oxygen does not stop you yawning.',
          'The better current guess is that a yawn cools the brain slightly, which fits the '
          'timing: people yawn most when tired, bored, or overheated.']},
 ],
},

# ---------------------------------------------------------------- 09
{
 'slug': 'blocked-nose-taste',
 'kicker': 'Food',
 'hue': 'coral',
 'title': 'Why does food taste like nothing with a cold?',
 'teaser': 'Most of what you call taste was never taste in the first place.',
 'answer': 'Your tongue reports five things: sweet, salty, sour, bitter and savoury. '
           'Strawberry, coffee, roast chicken — those are all smell, picked up from the '
           'back of your throat. Block the nose and only the five are left.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <path d="M14 30h26v11a11 11 0 0 1-11 11h-4a11 11 0 0 1-11-11z" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <path d="M40 34h5a5 5 0 0 1 0 10h-5" fill="none" stroke="var(--bright)" stroke-width="3"/>
  <path d="M22 22c0-4 4-5 4-9M31 22c0-4 4-5 4-9" fill="none" stroke="var(--bright)" stroke-width="2.5" stroke-linecap="round" opacity=".6"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 330" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Flavour notes disappearing when the nose is blocked</title>
  <circle cx="330" cy="165" r="56" class="f-soft" stroke="var(--bright)" stroke-width="2.5"/>
  <text x="330" y="160" text-anchor="middle" class="f-value" style="font-size:16px">STRAWBERRY</text>
  <text x="330" y="182" text-anchor="middle" class="f-label" id="coreLbl">tastes like</text>
  <g id="notes"></g>
</svg>''',
 'controls': '''<div class="switch" role="group" aria-label="Your nose">
  <button id="nClear" aria-pressed="true">Nose clear</button>
  <button id="nBlock" aria-pressed="false">Nose blocked</button>
</div>
<div class="control" style="flex:0 0 auto">
  <label>What you can tell apart</label>
  <span class="readout" id="countOut">&#8212;</span>
</div>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
// the five the tongue can do on its own, plus the ones that are really smell
var NOTES = [
  ['Sweet', true], ['Sour', true], ['Salty', true], ['Bitter', true], ['Savoury', true],
  ['Jammy', false], ['Green', false], ['Floral', false], ['Ripe', false],
  ['Fresh-cut', false], ['Candy', false], ['Earthy', false]
];
var notes = document.getElementById('notes'), items = [];
NOTES.forEach(function (n, i) {
  var a = (i / NOTES.length) * Math.PI * 2 - Math.PI / 2;
  var x = 330 + Math.cos(a) * 128, y = 165 + Math.sin(a) * 128;
  var g = document.createElementNS(NS, 'g');
  g.innerHTML =
    '<rect x="' + (x - 46) + '" y="' + (y - 15) + '" width="92" height="30" rx="15" fill="#fff" stroke="var(--border)" stroke-width="1.5"/>' +
    '<text x="' + x + '" y="' + (y + 5) + '" text-anchor="middle" class="f-label">' + n[0] + '</text>';
  notes.appendChild(g);
  items.push({ g: g, tongue: n[1] });
});

function setMode(blocked) {
  document.getElementById('nBlock').setAttribute('aria-pressed', blocked ? 'true' : 'false');
  document.getElementById('nClear').setAttribute('aria-pressed', blocked ? 'false' : 'true');
  var n = 0;
  items.forEach(function (it) {
    var showing = it.tongue || !blocked;
    it.g.setAttribute('opacity', showing ? '1' : '0.12');
    if (showing) n++;
    it.g.children[0].setAttribute('stroke', showing && it.tongue ? 'var(--bright)' : 'var(--border)');
  });
  document.getElementById('countOut').textContent = n + ' of ' + NOTES.length;
  document.getElementById('coreLbl').textContent = blocked ? 'sweet, and sour' : 'tastes like';
}
document.getElementById('nBlock').addEventListener('click', function () { setMode(true); });
document.getElementById('nClear').addEventListener('click', function () { setMode(false); });
setMode(false);
''',
 'caption': 'Block the nose. The five your tongue can manage stay lit; everything that '
            'made it recognisably strawberry goes out. The food has not changed at all.',
 'sections': [
   {'h': 'Taste and flavour are different things',
    'p': ['Taste is what the tongue does, and it is a short list: sweet, salty, sour, '
          'bitter and savoury. That is genuinely all of it.',
          'Flavour is that list <strong>plus smell</strong>, and smell carries almost all '
          'the detail. When you chew, air is pushed up the back of your throat into your '
          'nose. Your brain files what arrives that way as taste, because it happens while '
          'food is in your mouth.']},
   {'h': 'Try it without catching a cold',
    'p': ['Pinch your nose shut and eat a jelly sweet. You get sweet and sour, and no idea '
          'which flavour it was meant to be. Let go and the name of it arrives immediately.',
          'It works with coffee, wine and cinnamon too. A blocked nose is doing the same '
          'thing, just less politely.']},
   {'h': 'Why hospital food gets blamed unfairly',
    'p': ['Illness, some medicines, and simply getting older all dull smell before they dull '
          'taste. Food starts seeming bland and over-salted at the same time.',
          'Cooks work around it with things the tongue can still reach — acid, salt, chilli '
          'heat — rather than more aroma, which is not landing.']},
 ],
},

# ---------------------------------------------------------------- 10
{
 'slug': 'wifi-dead-zone',
 'kicker': 'Tech',
 'hue': 'blue',
 'title': 'Why is the wifi terrible in one room?',
 'teaser': 'Where the router sits matters more than what you paid for it.',
 'answer': 'Wifi is radio, and it loses strength going through walls — worst of all thick '
           'or wet ones. A router in the corner spends half its signal on next door. '
           'Moving it to the middle, out in the open, usually fixes the bad room.',
 'icon': '''<svg viewBox="0 0 64 64" aria-hidden="true">
  <circle cx="32" cy="46" r="4" fill="var(--bright)"/>
  <path d="M21 36a15 15 0 0 1 22 0" fill="none" stroke="var(--bright)" stroke-width="3" stroke-linecap="round"/>
  <path d="M13 27a26 26 0 0 1 38 0" fill="none" stroke="var(--bright)" stroke-width="3" stroke-linecap="round" opacity=".55"/>
</svg>''',
 'svg': '''<svg viewBox="0 0 660 340" role="img" aria-labelledby="figTitle">
  <title id="figTitle">A flat plan showing signal strength in each room</title>
  <g id="rooms"></g>
  <rect x="40" y="30" width="580" height="270" rx="10" fill="none" stroke="var(--ink)" stroke-width="3"/>
  <line x1="330" y1="30" x2="330" y2="300" stroke="var(--ink)" stroke-width="3"/>
  <line x1="40" y1="165" x2="620" y2="165" stroke="var(--ink)" stroke-width="3"/>
  <circle id="router" cx="150" cy="90" r="11" class="f-fill"/>
  <circle id="halo" cx="150" cy="90" r="26" fill="none" stroke="var(--bright)" stroke-width="2" opacity=".45"/>
</svg>''',
 'controls': '''<div class="control">
  <label for="rx">Router left / right</label>
  <input type="range" id="rx" min="60" max="600" step="5" value="150">
</div>
<div class="control">
  <label for="ry">Router up / down</label>
  <input type="range" id="ry" min="50" max="280" step="5" value="90">
</div>
<div class="control" style="flex:0 0 auto">
  <label>Worst room</label>
  <span class="readout" id="worstOut">&#8212;</span>
</div>''',
 'js': '''
var NS = 'http://www.w3.org/2000/svg';
var rx = document.getElementById('rx'), ry = document.getElementById('ry');
var ROOMS = [
  { name: 'Kitchen',  x: 40,  y: 30,  w: 290, h: 135 },
  { name: 'Bedroom',  x: 330, y: 30,  w: 290, h: 135 },
  { name: 'Living',   x: 40,  y: 165, w: 290, h: 135 },
  { name: 'Bathroom', x: 330, y: 165, w: 290, h: 135 }
];
var rooms = document.getElementById('rooms'), cells = [];
ROOMS.forEach(function (r) {
  var g = document.createElementNS(NS, 'g');
  g.innerHTML =
    '<rect x="' + r.x + '" y="' + r.y + '" width="' + r.w + '" height="' + r.h + '" fill="var(--wash)"/>' +
    '<text x="' + (r.x + 20) + '" y="' + (r.y + 34) + '" class="f-label">' + r.name.toUpperCase() + '</text>' +
    '<text x="' + (r.x + 20) + '" y="' + (r.y + 74) + '" class="f-value" style="font-size:22px">&#8212;</text>' +
    '<g class="bars"></g>';
  rooms.appendChild(g);
  cells.push({ r: r, rect: g.children[0], val: g.children[2], bars: g.children[3] });
});

function draw() {
  var x = +rx.value, y = +ry.value;
  document.getElementById('router').setAttribute('cx', x);
  document.getElementById('router').setAttribute('cy', y);
  document.getElementById('halo').setAttribute('cx', x);
  document.getElementById('halo').setAttribute('cy', y);

  var worst = 100, worstName = '';
  cells.forEach(function (c) {
    var cx = c.r.x + c.r.w / 2, cy = c.r.y + c.r.h / 2;
    var d = Math.hypot(cx - x, cy - y);
    // each wall the signal crosses costs far more than distance does
    var walls = ((x < 330) !== (cx < 330) ? 1 : 0) + ((y < 165) !== (cy < 165) ? 1 : 0);
    var s = 100 - d * 0.13 - walls * 26;
    s = Math.max(4, Math.min(100, s));
    if (s < worst) { worst = s; worstName = c.r.name; }

    c.rect.setAttribute('fill', s > 65 ? 'var(--wash)' : '#fff');
    c.val.textContent = s > 75 ? 'Great' : s > 50 ? 'Fine' : s > 28 ? 'Patchy' : 'Dead';
    // .f-value already sets fill in the stylesheet, and a class beats a
    // presentation attribute — so this has to go through style to land
    c.val.style.fill = s > 50 ? 'var(--hue-ink)' : 'var(--muted)';

    var b = '';
    for (var i = 0; i < 4; i++) {
      var lit = s > i * 25;
      b += '<rect x="' + (c.r.x + 20 + i * 14) + '" y="' + (c.r.y + 90 + (3 - i) * 5) +
           '" width="9" height="' + (10 + i * 5) + '" rx="2" fill="' +
           (lit ? 'var(--bright)' : 'var(--border)') + '"/>';
    }
    c.bars.innerHTML = b;
  });
  document.getElementById('worstOut').textContent = worstName;
}
rx.addEventListener('input', draw);
ry.addEventListener('input', draw);
draw();
''',
 'caption': 'Slide the router around the flat. Notice how much more it costs to cross a '
            'wall than to travel across an open room — the corner is nearly always the '
            'worst spot you could pick.',
 'sections': [
   {'h': 'Walls cost more than distance',
    'p': ['Open air barely troubles a wifi signal. A solid wall can take a big bite out of '
          'it, and brick, concrete, tile and anything with water or metal in it are far '
          'worse than a plasterboard partition.',
          'That is why a room fifteen feet away through two walls can be much worse than a '
          'room forty feet away down a hallway. <strong>Count walls, not metres.</strong>']},
   {'h': 'The corner problem',
    'p': ['A router radiates roughly all around itself. Put it in the corner of the flat and '
          'a large share of that is going straight out into the street or your neighbours.',
          'Move it toward the middle and the same router covers far more of your home, '
          'without spending anything.']},
   {'h': 'Before you buy anything', 'tips': [
     'Move the router to the middle of the home, out in the open, off the floor.',
     'Keep it away from the microwave, the fish tank and big metal appliances.',
     'Use the 5 GHz network up close for speed, and 2.4 GHz further away — it travels better through walls.',
     'If one room is still dead, a mesh point or a wired access point beats a bigger router.']},
 ],
},

]
