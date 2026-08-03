# -*- coding: utf-8 -*-
"""Every story Context tells. One dict each; build.py does the rest.

The shape is deliberately a story, not an article:

    standfirst  the hook — why you should care, in one breath
    beats       the build, in order
    turn        the pivot. one line, set big. the thing you came for
    figure      the moment you stop reading and operate the idea yourself
    zoomout     the landing. what it means once the fact has sunk in

Fields:
    slug     url + filename
    kicker   category. new ones are free — the nav builds itself
    tone     nebula | deepsea | ember | forest | dusk | solar
    scene    stars | orbit | swarm | waves | bloom  (the canvas backdrop)
    featured shown on the home page
"""

STORIES = [

# ------------------------------------------------------------------ #
{
 'slug': 'falling-into-a-black-hole',
 'kicker': 'Space',
 'tone': 'nebula',
 'scene': 'orbit',
 'featured': True,
 'title': 'What it is like to fall into a black hole',
 'teaser': 'You would not be crushed at the edge. For a while it would look like nothing was happening at all.',
 'standfirst': 'There is no wall, no alarm, no moment where you feel yourself cross. '
               'The strangest part of falling into a black hole is how ordinary it '
               'would feel while it happened.',

 'beats': [
   {'h': 'The edge is not a thing you can touch',
    'p': ['A black hole is drawn as a hole with a rim, so most of us imagine arriving '
          'somewhere — a surface, a membrane, something that resists.',
          'There is nothing there. The event horizon is not made of matter. It is a '
          'distance, marked out in empty space, and if you fell through it you would '
          'notice <strong>absolutely nothing</strong> at the moment you did. No jolt. '
          'No boundary. The stars would still be ahead of you.']},

   {'h': 'Meanwhile, everyone watching sees something else entirely',
    'p': ['To anyone far away, you never arrive. You fall more and more slowly, your '
          'image reddening and dimming, until you are frozen just short of the edge, '
          'fading toward black.',
          'Both of these are true at once. You fall straight through in a few seconds. '
          'They watch you hang there for the rest of time. Neither of you is mistaken.']},
 ],

 'turn': 'The horizon is not a place. It is a deadline.',

 'after': [
   {'h': 'What actually gets you',
    'p': ['The danger is not the crossing, it is the stretching. Gravity pulls your feet '
          'harder than your head, and close enough in, that difference becomes larger '
          'than the forces holding you together.',
          'Here is the part nobody expects: <strong>the bigger the black hole, the '
          'gentler the edge.</strong> Fall into a small one and you are pulled apart '
          'long before you reach it. Fall into a supermassive one and you sail across '
          'the horizon comfortably intact — and only then does the trap close.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 320" role="img" aria-labelledby="figTitle">
  <title id="figTitle">A clock falling toward a black hole, and how its time compares to yours</title>
  <defs>
    <radialGradient id="bh" cx="50%" cy="50%">
      <stop offset="55%" stop-color="#000"/>
      <stop offset="78%" stop-color="rgba(255,255,255,.35)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0)"/>
    </radialGradient>
  </defs>
  <circle cx="120" cy="160" r="88" fill="url(#bh)"/>
  <circle cx="120" cy="160" r="52" fill="#000"/>
  <circle id="horizon" cx="120" cy="160" r="52" fill="none" stroke="rgba(255,255,255,.55)" stroke-dasharray="4 5"/>
  <text class="f-label" x="120" y="272" text-anchor="middle">EVENT HORIZON</text>

  <circle id="faller" cx="420" cy="160" r="11" fill="#fff"/>
  <line id="track" class="f-faint" x1="172" y1="160" x2="600" y2="160"/>

  <text class="f-label" x="330" y="52">ONE SECOND ON YOUR CLOCK LASTS</text>
  <text class="f-value" id="dilTxt" x="330" y="92" style="font-size:30px">1.0 s out here</text>

  <text class="f-label" x="330" y="232">THEY SEE YOUR LIGHT SHIFT TO</text>
  <rect id="swatch" x="330" y="244" width="52" height="26" rx="8" fill="#fff"/>
  <text class="f-value" id="colTxt" x="396" y="263">unchanged</text>
</svg>''',
  'controls': '''<div class="control">
  <label for="dist">Distance from the horizon</label>
  <input type="range" id="dist" min="101" max="800" step="1" value="400">
  <span class="readout" id="distOut">4.00 radii</span>
</div>''',
  'js': '''
var dist = document.getElementById('dist');

function draw() {
  var r = +dist.value / 100;                 // in Schwarzschild radii, always > 1
  document.getElementById('distOut').textContent = r.toFixed(2) + ' radii';

  // gravitational time dilation outside a non-rotating black hole
  var f = 1 / Math.sqrt(1 - 1 / r);

  document.getElementById('dilTxt').textContent =
    f > 60 ? 'basically forever' : f.toFixed(1) + ' s out here';

  // put the faller where the slider says, measured from the horizon
  var x = 120 + 52 * r;
  document.getElementById('faller').setAttribute('cx', Math.min(x, 640));

  // light climbing out is stretched by the same factor
  var sw = document.getElementById('swatch'), col = document.getElementById('colTxt');
  if (f < 1.15)      { sw.setAttribute('fill', '#ffffff'); col.textContent = 'barely changed'; }
  else if (f < 1.6)  { sw.setAttribute('fill', '#ffe9a3'); col.textContent = 'warm yellow'; }
  else if (f < 2.6)  { sw.setAttribute('fill', '#ff9d5c'); col.textContent = 'orange'; }
  else if (f < 6)    { sw.setAttribute('fill', '#f2554a'); col.textContent = 'deep red'; }
  else if (f < 20)   { sw.setAttribute('fill', '#7a1533'); col.textContent = 'infrared, invisible'; }
  else               { sw.setAttribute('fill', '#1a0a14'); col.textContent = 'gone'; }
}
dist.addEventListener('input', draw);
draw();
''',
  'caption': 'Slide yourself toward the horizon. Your own clock never changes — it ticks '
             'once a second, exactly as it always has. Everything on this readout is what '
             'the rest of the universe sees.'
 },

 'zoomout': 'We expect the universe to announce its important moments. It does not. The '
            'most consequential boundary anyone could ever cross is unmarked, unguarded '
            'and completely silent, and you would sail through it wondering when you were '
            'going to arrive.',
},

# ------------------------------------------------------------------ #
{
 'slug': 'mostly-not-you',
 'kicker': 'Your body',
 'tone': 'forest',
 'scene': 'swarm',
 'featured': True,
 'title': 'You are mostly not you',
 'teaser': 'About half the cells you are carrying are not human. They are not passengers either.',
 'standfirst': 'Right now you are carrying roughly as many bacterial cells as human ones. '
               'They are not along for the ride — a good deal of what you think of as '
               'your body is work they are doing.',

 'beats': [
   {'h': 'The numbers are closer than anyone expected',
    'p': ['For decades the popular figure was ten bacteria for every human cell. It was a '
          'back-of-an-envelope estimate from 1972 that nobody re-checked for forty years.',
          'When it was finally done properly the answer came out at roughly <strong>one to '
          'one</strong> — about thirty trillion human cells and about thirty-eight trillion '
          'bacteria. Still an astonishing number of tenants.']},

   {'h': 'They weigh almost nothing',
    'p': ['All of them together come to about two hundred grams. A small apple. Bacteria '
          'are so much smaller than your cells that tens of trillions of them barely '
          'register on a scale.',
          'And they are not spread evenly. Your blood is meant to be sterile. Your skin '
          'carries a thin film. Almost the entire population is packed into your large '
          'intestine.']},
 ],

 'turn': 'You are not an individual. You are a negotiation.',

 'after': [
   {'h': 'What you are getting out of the arrangement',
    'p': ['They break down fibre you have no enzymes for, releasing energy you would '
          'otherwise walk past. They manufacture vitamin K and several B vitamins. They '
          'occupy the space that a dangerous organism would otherwise take.',
          'They also spend your childhood training your immune system on what to ignore. '
          'Grow up without that training and the system becomes twitchy — which is one of '
          'the better explanations we have for why allergies climb as places get cleaner.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Where your microbes actually live</title>
  <g id="field"></g>
  <text class="f-label" x="20" y="34" id="placeLbl">GUT</text>
  <text class="f-label" x="20" y="238">MICROBES PER HUMAN CELL HERE</text>
  <text class="f-value" id="ratioTxt" x="20" y="274" style="font-size:28px">&#8212;</text>
  <text class="f-label" x="380" y="238">SHARE OF ALL YOUR MICROBES</text>
  <text class="f-value" id="shareTxt" x="380" y="274" style="font-size:28px">&#8212;</text>
</svg>''',
  'controls': '''<div class="chips" role="group" aria-label="Part of the body">
  <button class="chip" id="pGut" aria-pressed="true">Large intestine</button>
  <button class="chip" id="pMouth" aria-pressed="false">Mouth</button>
  <button class="chip" id="pSkin" aria-pressed="false">Skin</button>
  <button class="chip" id="pBlood" aria-pressed="false">Blood</button>
</div>''',
  'js': '''
var NS = 'http://www.w3.org/2000/svg';
// ratio = microbes per human cell; share = portion of your total microbe count
var PLACES = {
  pGut:   { name: 'LARGE INTESTINE', ratio: 1000, share: 99,   label: 'about 1,000' },
  pMouth: { name: 'MOUTH',           ratio: 1,    share: 0.5,  label: 'about 1' },
  pSkin:  { name: 'SKIN',            ratio: 0.1,  share: 0.1,  label: 'about 1 in 10' },
  pBlood: { name: 'BLOOD',           ratio: 0,    share: 0,    label: 'none, if you are well' }
};

var field = document.getElementById('field'), dots = [];
for (var i = 0; i < 240; i++) {
  var c = document.createElementNS(NS, 'circle');
  var col = i % 24, row = (i / 24) | 0;
  c.setAttribute('cx', 30 + col * 26);
  c.setAttribute('cy', 62 + row * 15);
  c.setAttribute('r', 5);
  field.appendChild(c);
  dots.push(c);
}

function show(key) {
  var p = PLACES[key];
  Object.keys(PLACES).forEach(function (k) {
    document.getElementById(k).setAttribute('aria-pressed', k === key ? 'true' : 'false');
  });
  document.getElementById('placeLbl').textContent = p.name;
  document.getElementById('ratioTxt').textContent = p.label;
  document.getElementById('shareTxt').textContent =
    p.share === 0 ? 'none' : p.share >= 1 ? p.share + '%' : 'under 1%';

  // fill the field to match the ratio, capped so the picture stays readable
  var frac = p.ratio === 0 ? 0 : Math.min(1, p.ratio / (p.ratio + 1));
  dots.forEach(function (d, i) {
    var microbe = i / dots.length < frac;
    d.setAttribute('fill', microbe ? '#fff' : 'rgba(255,255,255,.22)');
    d.setAttribute('r', microbe ? 4 : 6);
  });
}

Object.keys(PLACES).forEach(function (k) {
  document.getElementById(k).addEventListener('click', function () { show(k); });
});
show('pGut');
''',
  'caption': 'Small bright dots are microbes, large faint ones are your own cells. Your '
             'blood should come up empty — anything living in there is an emergency.'
 },

 'zoomout': 'It is tempting to file this under unsettling. It is closer to the opposite. '
            'Nothing complicated on this planet made it alone, and the boundary you draw '
            'around yourself is a convenience rather than a fact.',
},

# ------------------------------------------------------------------ #
{
 'slug': 'made-of-dead-stars',
 'kicker': 'Origins',
 'tone': 'dusk',
 'scene': 'stars',
 'featured': True,
 'title': 'Everything you are was made inside a star',
 'teaser': 'The calcium in your bones and the iron in your blood could not exist until something enormous died.',
 'standfirst': 'The early universe could build almost nothing. Every atom in you heavier '
               'than helium had to be manufactured somewhere violent, and then thrown '
               'back out.',

 'beats': [
   {'h': 'The universe began with a very short shopping list',
    'p': ['For the first few minutes there was hydrogen, helium, and a trace of lithium. '
          'That is the entire inventory. No carbon, no oxygen, no iron, nothing to make '
          'a rock out of, let alone a person.',
          'Everything else had to be assembled later, one nucleus at a time, in the only '
          'places hot and heavy enough to do it.']},

   {'h': 'Stars are furnaces that eventually fail',
    'p': ['A star spends its life fusing light elements into heavier ones. Hydrogen into '
          'helium, then helium into carbon and oxygen, each stage hotter and faster than '
          'the last.',
          'Then it hits iron. Fusing iron <strong>costs</strong> energy instead of '
          'releasing it, so the furnace stalls, the core collapses, and the star tears '
          'itself apart — scattering everything it ever made.']},
 ],

 'turn': 'Every atom in you heavier than helium was somewhere else violent first.',

 'after': [
   {'h': 'And some of it needed something even rarer',
    'p': ['Supernovae cannot account for all of it. The heaviest elements — gold, '
          'platinum, the iodine your thyroid runs on — appear to come mostly from '
          'neutron stars colliding.',
          'We watched that happen for the first time in 2017. Two dead stellar cores '
          'spiralled together and threw off a cloud containing, by some estimates, '
          'several Earth masses of gold.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Where each element in your body was manufactured</title>
  <circle id="src" cx="150" cy="150" r="66" fill="rgba(255,255,255,.14)" stroke="#fff" stroke-width="2"/>
  <text id="srcIcon" x="150" y="162" text-anchor="middle" class="f-value" style="font-size:38px">H</text>
  <text class="f-label" x="330" y="70">MADE IN</text>
  <text class="f-value" id="whereTxt" x="330" y="106" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="330" y="150">WHEN</text>
  <text class="f-value" id="whenTxt" x="330" y="182" style="font-size:20px">&#8212;</text>
  <text class="f-label" x="330" y="226">SHARE OF YOUR BODY, BY MASS</text>
  <rect x="330" y="240" width="300" height="18" rx="9" fill="rgba(255,255,255,.18)"/>
  <rect id="massBar" x="330" y="240" width="0" height="18" rx="9" fill="#fff"/>
  <text class="f-value" id="massTxt" x="330" y="286" style="font-size:18px">&#8212;</text>
</svg>''',
  'controls': '''<div class="chips" role="group" aria-label="Element">
  <button class="chip" id="eH" aria-pressed="true">Hydrogen</button>
  <button class="chip" id="eO" aria-pressed="false">Oxygen</button>
  <button class="chip" id="eC" aria-pressed="false">Carbon</button>
  <button class="chip" id="eCa" aria-pressed="false">Calcium</button>
  <button class="chip" id="eFe" aria-pressed="false">Iron</button>
  <button class="chip" id="eI" aria-pressed="false">Iodine</button>
</div>''',
  'js': '''
var EL = {
  eH:  { s: 'H',  mass: 10.0, where: 'The Big Bang',            when: 'the first few minutes' },
  eO:  { s: 'O',  mass: 65.0, where: 'Massive stars',           when: 'billions of years ago' },
  eC:  { s: 'C',  mass: 18.5, where: 'Dying low-mass stars',    when: 'billions of years ago' },
  eCa: { s: 'Ca', mass: 1.5,  where: 'Supernovae',              when: 'before the Sun existed' },
  eFe: { s: 'Fe', mass: 0.006, where: 'Supernovae',             when: 'before the Sun existed' },
  eI:  { s: 'I',  mass: 0.00002, where: 'Neutron stars colliding', when: 'rare, and very long ago' }
};

function show(key) {
  var e = EL[key];
  Object.keys(EL).forEach(function (k) {
    document.getElementById(k).setAttribute('aria-pressed', k === key ? 'true' : 'false');
  });
  document.getElementById('srcIcon').textContent = e.s;
  document.getElementById('whereTxt').textContent = e.where;
  document.getElementById('whenTxt').textContent = e.when;
  // log scale, or hydrogen and iodine cannot share an axis
  var w = Math.max(4, (Math.log10(e.mass) + 5) / 6 * 300);
  document.getElementById('massBar').setAttribute('width', Math.min(w, 300));
  document.getElementById('massTxt').textContent =
    e.mass >= 1 ? e.mass + '%' : e.mass >= 0.001 ? e.mass + '%' : 'a trace, and you die without it';
}

Object.keys(EL).forEach(function (k) {
  document.getElementById(k).addEventListener('click', function () { show(k); });
});
show('eH');
''',
  'caption': 'The bar is on a log scale — oxygen and iodine are separated by six orders of '
             'magnitude, and a linear axis would render iodine invisible. Which would rather '
             'miss the point.'
 },

 'zoomout': 'This is not a metaphor and it is not a nice way of putting things. The iron '
            'moving oxygen around your body this second was forged in a collapsing star '
            'and flung across the galaxy before the Sun had formed. It ended up here.',
},

# ------------------------------------------------------------------ #
{
 'slug': 'if-everyone-jumped',
 'kicker': 'Big numbers',
 'tone': 'ember',
 'scene': 'waves',
 'featured': False,
 'title': 'What if everyone on Earth jumped at once?',
 'teaser': 'Eight billion people, one jump, the same instant. The planet would barely notice — and that is the interesting bit.',
 'standfirst': 'It is the kind of question that sounds like it should have a dramatic '
               'answer. Working out why it does not tells you something useful about '
               'the size of things.',

 'beats': [
   {'h': 'Eight billion sounds like enough',
    'p': ['It is a genuinely enormous number of people. Stand them shoulder to shoulder '
          'and they would cover a good-sized city. Add up their mass and you get around '
          'half a billion tonnes.',
          'The intuition says that much weight, moving together, must do <em>something</em>.']},

   {'h': 'The Earth is playing a different game',
    'p': ['The planet weighs about six thousand billion billion tonnes. Every human alive '
          'adds up to roughly one part in thirteen trillion of it.',
          'When you jump, the Earth does push back — momentum is conserved and it genuinely '
          'recoils. It just recoils by an amount that has no business being called a '
          'distance.']},
 ],

 'turn': 'The whole planet would shift by a fraction of the width of a single atom, then shift back.',

 'after': [
   {'h': 'The dangerous part was never the jump',
    'p': ['If you actually assembled eight billion people in one place to try it, the '
          'gathering would be the catastrophe. There is no way to feed, water or move '
          'that crowd, and no ground that stays intact underneath it.',
          'The jump itself is a rounding error. Getting everyone to the same field is the '
          'end of the world.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How far the Earth recoils when people jump</title>
  <circle cx="150" cy="170" r="80" fill="rgba(255,255,255,.16)" stroke="#fff" stroke-width="2"/>
  <text x="150" y="178" text-anchor="middle" class="f-value" style="font-size:20px">EARTH</text>
  <g id="jumpers"></g>
  <text class="f-label" x="330" y="60">THE EARTH MOVES</text>
  <text class="f-value" id="moveTxt" x="330" y="98" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="330" y="150">FOR COMPARISON, ONE ATOM IS</text>
  <text class="f-value" id="cmpTxt" x="330" y="184" style="font-size:20px">&#8212;</text>
  <text class="f-label" x="330" y="232">SO THE SHIFT IS</text>
  <text class="f-value" id="fracTxt" x="330" y="266" style="font-size:20px">&#8212;</text>
</svg>''',
  'controls': '''<div class="control">
  <label for="ppl">People jumping</label>
  <input type="range" id="ppl" min="0" max="100" step="1" value="100">
  <span class="readout" id="pplOut">8.0 billion</span>
</div>''',
  'js': '''
var NS = 'http://www.w3.org/2000/svg';
var ppl = document.getElementById('ppl');

var M_EARTH = 5.972e24;      // kg
var MASS = 62;               // kg, rough global average including children
var HEIGHT = 0.3;            // m, a decent standing jump
var ATOM = 1e-10;            // m, near enough for a comparison

var jump = document.getElementById('jumpers'), figs = [];
for (var i = 0; i < 40; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 40 + (i % 20) * 11);
  c.setAttribute('cy', i < 20 ? 60 : 80);
  c.setAttribute('r', 3.5);
  c.setAttribute('fill', '#fff');
  jump.appendChild(c);
  figs.push(c);
}

function draw() {
  var frac = +ppl.value / 100;
  var n = frac * 8e9;
  document.getElementById('pplOut').textContent =
    n < 1e6 ? Math.round(n).toLocaleString('en-GB') : (n / 1e9).toFixed(1) + ' billion';

  // centre of mass stays put, so Earth's shift = (their mass / Earth's) x jump height
  var d = (n * MASS / M_EARTH) * HEIGHT;

  document.getElementById('moveTxt').textContent =
    d === 0 ? 'not at all' : d.toExponential(1).replace('e-', ' x 10^-') + ' m';
  document.getElementById('cmpTxt').textContent = '0.0000000001 m across';
  document.getElementById('fracTxt').textContent =
    d === 0 ? '&#8212;' : (d / ATOM < 0.001
      ? 'under a thousandth of an atom'
      : (d / ATOM).toFixed(4) + ' of one atom');

  figs.forEach(function (f, i) {
    f.setAttribute('opacity', i / figs.length < frac ? 1 : 0.15);
  });
}
ppl.addEventListener('input', draw);
draw();
''',
  'caption': 'Turn everybody out and the number still refuses to become impressive. The '
             'answer is written in scientific notation because there is no ordinary unit '
             'small enough to say it in.'
 },

 'zoomout': 'Our sense of "a lot" tops out early. Eight billion is past the point where '
            'the feeling of hugeness stops tracking the arithmetic, which is exactly why '
            'the question feels like it ought to have a bigger answer than it does.',
},

# ------------------------------------------------------------------ #
{
 'slug': 'the-suns-timetable',
 'kicker': 'Time',
 'tone': 'solar',
 'scene': 'bloom',
 'featured': True,
 'title': 'The Sun has a schedule, and we are on it',
 'teaser': 'It will not explode. What it will actually do is slower, stranger, and already under way.',
 'standfirst': 'The Sun is not a fixed background object. It has been steadily brightening '
               'your whole life, and the thing that ends life on Earth is not its death '
               'but its middle age.',

 'beats': [
   {'h': 'It is roughly halfway through',
    'p': ['The Sun formed about 4.6 billion years ago and has fuel for something like ten '
          'billion. In stellar terms it is comfortably middle-aged and completely '
          'unremarkable, which is good news for us.',
          'It is also not the sort of star that explodes. It is far too light. It will end '
          'quietly.']},

   {'h': 'But it is getting brighter, now',
    'p': ['As the core fuses hydrogen into helium it gets denser, which makes it hotter, '
          'which makes the whole star put out more energy. The Sun is roughly 30% brighter '
          'than when it formed, and it climbs about 1% every hundred million years.',
          'That sounds gentle. It is not. In something like a billion years the extra heat '
          'is enough to push Earth past the point where oceans stay liquid — while the Sun '
          'is still an ordinary, healthy, middle-aged star.']},
 ],

 'turn': 'Earth does not have a Sun-death problem. It has a Sun-middle-age problem, and the deadline is a billion years out.',

 'after': [
   {'h': 'And then, eventually, the big finish',
    'p': ['At around ten billion years the core runs out of hydrogen and the Sun swells '
          'into a red giant, several hundred times its current size. Mercury and Venus go. '
          'Earth is probably swallowed too, and if it is not, it is scorched bare.',
          'Then the outer layers drift off and what is left is a white dwarf the size of '
          'the Earth: no fusion, no light of its own, just a cooling ember that will still '
          'be out there, dimming, for trillions of years.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 320" role="img" aria-labelledby="figTitle">
  <title id="figTitle">The Sun's size and Earth's fate across its lifetime</title>
  <defs>
    <radialGradient id="glowGrad">
      <stop id="glowIn" offset="55%" stop-color="#FFD36E" stop-opacity=".45"/>
      <stop id="glowOut" offset="100%" stop-color="#FFD36E" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle id="sunGlow" cx="170" cy="170" r="56" fill="url(#glowGrad)"/>
  <circle id="sun" cx="170" cy="170" r="40" fill="#FFD36E"/>
  <circle id="earth" cx="300" cy="170" r="7" fill="#7FC7FF"/>
  <text class="f-label" x="300" y="196" text-anchor="middle">EARTH</text>
  <line class="f-faint" x1="60" y1="286" x2="620" y2="286"/>
  <circle id="marker" cx="60" cy="286" r="6" fill="#fff"/>
  <text class="f-label" x="60" y="308">BIRTH</text>
  <text class="f-label" x="620" y="308" text-anchor="end">12 BILLION YEARS</text>
  <text class="f-label" x="420" y="60">THE SUN IS</text>
  <text class="f-value" id="phaseTxt" x="420" y="94" style="font-size:20px">&#8212;</text>
  <text class="f-label" x="420" y="136">EARTH IS</text>
  <text class="f-value" id="earthTxt" x="420" y="170" style="font-size:20px">&#8212;</text>
</svg>''',
  'controls': '''<div class="control">
  <label for="age">Age of the Sun</label>
  <input type="range" id="age" min="0" max="120" step="1" value="46">
  <span class="readout" id="ageOut">4.6 bn years</span>
</div>
<button class="chip" id="now" aria-pressed="false">Jump to today</button>''',
  'js': '''
var age = document.getElementById('age');

function draw() {
  var g = +age.value / 10;                 // billions of years since the Sun formed
  document.getElementById('ageOut').textContent = g.toFixed(1) + ' bn years';
  document.getElementById('marker').setAttribute('cx', 60 + (g / 12) * 560);

  var r, phase, earth;
  if (g < 10) {
    // main sequence: slow brightening, size almost flat
    r = 40 * (1 + g * 0.03);
    phase = 'a main-sequence star';
    earth = g < 5.6 ? 'habitable' :
            g < 8   ? 'losing its oceans' : 'a dry rock';
  } else if (g < 11) {
    var k = (g - 10);                      // the swelling happens fast
    r = 40 + k * 210;
    phase = 'a swelling red giant';
    earth = k < 0.5 ? 'scorched' : 'inside the Sun';
  } else {
    r = 6;
    phase = 'a cooling white dwarf';
    earth = 'gone, or a bare cinder';
  }

  var sun = document.getElementById('sun');
  sun.setAttribute('r', Math.min(r, 150));
  sun.setAttribute('fill', g >= 11 ? '#CFE8FF' : g >= 10 ? '#FF8A5B' : '#FFD36E');
  // the glow fades to transparent, so the viewBox can crop it without
  // leaving a visible hard edge
  var tint = g >= 11 ? '#CFE8FF' : g >= 10 ? '#FF8A5B' : '#FFD36E';
  document.getElementById('glowIn').setAttribute('stop-color', tint);
  document.getElementById('glowOut').setAttribute('stop-color', tint);
  document.getElementById('sunGlow').setAttribute('r', Math.min(r * 1.45, 260));

  document.getElementById('phaseTxt').textContent = phase;
  document.getElementById('earthTxt').textContent = earth;
  document.getElementById('earth').setAttribute('opacity', g >= 10.5 ? 0.15 : 1);
}
age.addEventListener('input', draw);
document.getElementById('now').addEventListener('click', function () {
  age.value = 46; draw();
});
draw();
''',
  'caption': 'Today sits at 4.6 billion years, and the Sun looks like it will do this '
             'forever. Drag past 5.6 and the trouble starts while the star is still, by '
             'every measure, perfectly healthy.'
 },

 'zoomout': 'A billion years is not a warning about anything you need to do this week. It '
            'is a reminder that "permanent" is a setting on human clocks only — even the '
            'thing we use as a synonym for constancy is on a schedule.',
},

# ------------------------------------------------------------------ #
{
 'slug': 'more-trees-than-stars',
 'kicker': 'Earth',
 'tone': 'deepsea',
 'scene': 'swarm',
 'featured': False,
 'title': 'There are more trees on Earth than stars in the galaxy',
 'teaser': 'About three trillion trees. About two hundred billion stars. It is not close.',
 'standfirst': 'For years the estimate was around 400 billion trees. Then somebody counted '
               'properly, and the number came back nearly eight times larger — and still '
               'far below what it used to be.',

 'beats': [
   {'h': 'The count nobody had actually done',
    'p': ['Estimating trees from satellites alone gives you canopy, not trunks. In 2015 a '
          'team combined half a million ground counts with satellite data and got a very '
          'different answer: about <strong>three trillion</strong> trees.',
          'The Milky Way, for comparison, holds somewhere between 100 and 400 billion '
          'stars. Even at the generous end, Earth is winning by a factor of ten.']},

   {'h': 'The same study found the other number',
    'p': ['Working backwards, they also estimated what the figure had been before humans '
          'started clearing land. It was roughly six trillion.',
          'We are not looking at a big number. We are looking at what is left of a much '
          'bigger one, and about fifteen billion trees still come down each year.']},
 ],

 'turn': 'For every star in the Milky Way, Earth grows about ten trees. It used to grow twenty.',

 'after': [
   {'h': 'Why the comparison is worth making at all',
    'p': ['Stars feel like the standard unit of "too many to count", and trees feel '
          'countable — they are the things at the end of your road.',
          'Getting it backwards is the useful part. Our sense of scale is built on how '
          'far away something is and how impressive it sounds, not on quantity, and it '
          'will mislead you in both directions.']},
 ],

 'figure': {
  'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Tree numbers over time against the stars in the Milky Way</title>
  <text class="f-label" x="20" y="34">TREES ON EARTH</text>
  <rect x="20" y="48" width="620" height="34" rx="17" fill="rgba(255,255,255,.16)"/>
  <rect id="treeBar" x="20" y="48" width="0" height="34" rx="17" fill="#fff"/>
  <text class="f-value" id="treeTxt" x="20" y="114" style="font-size:26px">&#8212;</text>

  <text class="f-label" x="20" y="168">STARS IN THE MILKY WAY (HIGH ESTIMATE)</text>
  <rect x="20" y="182" width="620" height="34" rx="17" fill="rgba(255,255,255,.16)"/>
  <rect x="20" y="182" width="41" height="34" rx="17" fill="rgba(255,255,255,.75)"/>
  <text class="f-value" x="20" y="248" style="font-size:26px">400 billion</text>
  <text class="f-label" id="ratioTxt" x="330" y="290" text-anchor="middle">&#8212;</text>
</svg>''',
  'controls': '''<div class="control">
  <label for="yr">Year</label>
  <input type="range" id="yr" min="-10000" max="2026" step="50" value="2026">
  <span class="readout" id="yrOut">2026</span>
</div>''',
  'js': '''
var yr = document.getElementById('yr');
var STARS = 400e9;          // generous end of the Milky Way estimate
var MAX = 6.2e12;           // bar is scaled to the pre-agriculture figure

function draw() {
  var y = +yr.value;
  document.getElementById('yrOut').textContent =
    y < 0 ? Math.abs(y).toLocaleString('en-GB') + ' BC' : y;

  // ~6 trillion before farming, ~3.04 trillion now, most of the loss recent
  var f = (y + 10000) / 12026;             // 0 at 10,000 BC, 1 today
  var trees = 6e12 - (6e12 - 3.04e12) * Math.pow(f, 3.2);

  document.getElementById('treeBar').setAttribute('width', 620 * trees / MAX);
  document.getElementById('treeTxt').textContent = (trees / 1e12).toFixed(2) + ' trillion';
  document.getElementById('ratioTxt').textContent =
    'that is ' + (trees / STARS).toFixed(1) + ' trees for every star';
}
yr.addEventListener('input', draw);
draw();
''',
  'caption': 'The star bar never moves; the galaxy is not going anywhere on this timescale. '
             'Drag back to before farming and watch how much of the difference we made in '
             'the last stretch.'
 },

 'zoomout': 'Both numbers are past the point where they mean anything to us directly. The '
            'difference is that one of them is still ours to change, and we have already '
            'changed it once.',
},

]
