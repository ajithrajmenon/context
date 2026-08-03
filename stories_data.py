# -*- coding: utf-8 -*-
"""Every story Context tells. One dict each; build.py does the rest.

Shape, taken from how the best explainer video essays are built:

    an opening image you can see before you understand it
    the question, asked plainly
    named chapters, each with its own picture AND ITS OWN COLOUR
    a checklist, where a thing has requirements
    the blocker — the reason it should not work
    the turn — one line, set big
    something you operate yourself
    a landing that stays humble

Colour belongs to the CARD, not the story. Each piece walks through four
to six tones as it goes, the way a film relights between acts.

Blocks:
    scene   full animated panel, one short line over it
    text    white card, a heading and a couple of short paragraphs
    steps   a numbered checklist
    turn    the pivot, big type on full colour
    figure  the interactive

Writing rules: short sentences, ordinary words, second person. A ten year
old should get through any of these without stopping.
"""

STORIES = [

# ================================================================== 01
{
 'slug': 'the-arrow-of-time',
 'kicker': 'Time',
 'card_tone': 'dusk', 'card_scene': 'entropy',
 'featured': True,
 'title': 'Why can you remember yesterday but not tomorrow?',
 'teaser': 'Almost every rule in physics works just as well backwards. So why does time only go one way?',
 'hero': {'tone': 'dusk', 'scene': 'entropy',
   'standfirst': 'Drop a cup and it shatters. No one has ever seen the pieces jump back '
                 'up and become a cup. Nothing in the rules forbids it — and yet it '
                 'never, ever happens.'},

 'blocks': [
  {'type': 'text', 'h': 'The rules do not care which way time runs',
   'p': ['Film two billiard balls hitting each other, then play it backwards. Both '
         'versions look completely normal. Nothing is broken.',
         'Now film the cup smashing and play <em>that</em> backwards. You know '
         'instantly that something is wrong.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'entropy',
   'h': 'One way to be tidy. Billions of ways to be a mess.',
   'p': 'That is the whole secret. There is nothing else to it.'},

  {'type': 'text', 'h': 'Think about a box of building blocks',
   'p': ['There is basically one way for them to be stacked in a perfect tower. There '
         'are an enormous number of ways for them to be scattered across the floor.',
         'Shake the box. You will almost certainly get a mess — not because mess is '
         'special, but because <strong>there is so much more of it</strong>.']},

  {'type': 'turn', 'tone': 'ember',
   'text': 'Time does not flow. Things just spread out, and we call that direction "forward".'},

  {'type': 'figure', 'tone': 'deepsea',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How many tidy arrangements there are compared to messy ones</title>
  <g id="blocks"></g>
  <text class="f-label" x="20" y="196">WAYS TO BE PERFECTLY TIDY</text>
  <text class="f-value" id="tidyTxt" x="20" y="232" style="font-size:30px">1</text>
  <text class="f-label" x="330" y="196">WAYS TO BE SOME KIND OF MESS</text>
  <text class="f-value" id="messTxt" x="330" y="232" style="font-size:30px">&#8212;</text>
  <text class="f-label" id="oddsTxt" x="20" y="278">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="n">How many blocks</label>
  <input type="range" id="n" min="2" max="20" step="1" value="6">
  <span class="readout" id="nOut">6</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var n = document.getElementById('n'), box = document.getElementById('blocks');

function fact(k) { var r = 1; for (var i = 2; i <= k; i++) r *= i; return r; }

function draw() {
  var k = +n.value;
  document.getElementById('nOut').textContent = k;
  box.textContent = '';
  var w = Math.min(46, 600 / k);
  for (var i = 0; i < k; i++) {
    var r = document.createElementNS(NS, 'rect');
    r.setAttribute('x', 20 + i * (w + 4));
    r.setAttribute('y', 60);
    r.setAttribute('width', w);
    r.setAttribute('height', 76);
    r.setAttribute('rx', 8);
    r.setAttribute('fill', 'rgba(255,255,255,.9)');
    box.appendChild(r);
  }
  // every ordering is equally likely; only one of them is "in order"
  var total = fact(k);
  document.getElementById('messTxt').textContent =
    total > 1e6 ? total.toExponential(1).replace('e+', ' x 10^') : (total - 1).toLocaleString('en-GB');
  document.getElementById('oddsTxt').textContent =
    'SHAKE THE BOX AND YOUR ODDS OF PERFECT ORDER ARE 1 IN ' +
    (total > 1e6 ? total.toExponential(1).replace('e+', ' x 10^') : total.toLocaleString('en-GB'));
}
n.addEventListener('input', draw);
draw();
''',
   'caption': 'Add blocks and watch the odds collapse. At twenty blocks you would need '
              'to shake the box more times than there have been seconds since the Big '
              'Bang. That is why the cup never comes back together.'},

  {'type': 'scene', 'tone': 'solar', 'scene': 'bloom',
   'h': 'Your memories point the same way',
   'p': 'Making a memory means putting something in order inside your head, and that '
        'always spills a little heat outward. You can only remember the direction the '
        'mess came from.'},

  {'type': 'text', 'h': 'So the past is not "gone"',
   'p': ['The past is simply the direction where things were more ordered. The future '
         'is the direction where they are more spread out.',
         'You remember yesterday because yesterday was tidier. There is no memory of '
         'tomorrow because tomorrow has not made its mess yet.']},
 ],

 'zoomout': {'tone': 'dusk',
   'text': 'Time turns out not to be a river carrying you along. It is just the fact '
           'that there are far more ways to be messy than tidy — repeated, everywhere, '
           'all at once, for fourteen billion years.'},
},

# ================================================================== 02
{
 'slug': 'how-big-is-the-universe',
 'kicker': 'Space',
 'card_tone': 'nebula', 'card_scene': 'expand',
 'featured': True,
 'title': 'How big is the universe, really?',
 'teaser': 'We can see for 46 billion light years. Most of what we can see, we can never reach.',
 'hero': {'tone': 'nebula', 'scene': 'expand',
   'standfirst': 'Look up on a clear night and you are looking backwards in time. The '
                 'further out you look, the older the picture — and there is a hard '
                 'edge to how far the looking can go.'},

 'blocks': [
  {'type': 'text', 'h': 'Light is fast, but it is not instant',
   'p': ['Sunlight takes eight minutes to reach you. You never see the Sun as it is, '
         'only as it was.',
         'For distant galaxies that delay becomes billions of years. You are looking '
         'at <strong>an old photograph</strong>, not a live feed.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'stars',
   'h': 'The universe is 13.8 billion years old',
   'p': 'So no light has had time to travel further than 13.8 billion years to get '
        'here. Anything beyond that has simply not arrived yet.'},

  {'type': 'text', 'h': 'But the edge is 46 billion light years away',
   'p': ['That sounds like a mistake. It is not. While the light was travelling, '
         '<strong>space itself was stretching</strong>, carrying its starting point '
         'further away behind it.',
         'The light took 13.8 billion years. The place it left is now 46 billion light '
         'years off.']},

  {'type': 'turn', 'tone': 'rose',
   'text': 'Space is not expanding into anything. There is no outside. It is the distances themselves that are growing.'},

  {'type': 'steps', 'tone': 'deepsea', 'h': 'Three different "sizes" people mean',
   'items': [
     {'h': 'What we can see', 'p': 'A ball 46 billion light years in every direction. Everything we will ever have evidence of.'},
     {'h': 'What we can reach', 'p': 'Far smaller. Beyond about 16 billion light years, space grows faster than we could ever chase it.'},
     {'h': 'The whole thing', 'p': 'Unknown, and possibly infinite. We are inside it, so we cannot step back and measure.'}]},

  {'type': 'figure', 'tone': 'nebula',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Whether a galaxy at a given distance can ever be reached</title>
  <circle cx="90" cy="150" r="10" fill="#fff"/>
  <text class="f-label" x="90" y="186" text-anchor="middle">US</text>
  <line class="f-faint" x1="90" y1="150" x2="630" y2="150"/>
  <circle id="gal" cx="300" cy="150" r="13" fill="rgba(255,255,255,.9)"/>
  <text class="f-label" x="20" y="42">HOW FAR AWAY</text>
  <text class="f-value" id="dTxt" x="20" y="76" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="330" y="42">CAN WE EVER GET THERE?</text>
  <text class="f-value" id="reachTxt" x="330" y="76" style="font-size:26px">&#8212;</text>
  <text class="f-label" id="seeTxt" x="20" y="248">&#8212;</text>
  <text class="f-label" id="ageTxt" x="20" y="278">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="d">Distance</label>
  <input type="range" id="d" min="1" max="60" step="1" value="10">
  <span class="readout" id="dOut">10 Bly</span>
</div>''',
   'js': '''
var d = document.getElementById('d');
var SEE = 46;      // edge of what we can observe, in billions of light years
var REACH = 16;    // beyond this, expansion outruns anything we could send

function draw() {
  var v = +d.value;
  document.getElementById('dOut').textContent = v + ' Bly';
  document.getElementById('dTxt').textContent = v + ' billion ly';
  document.getElementById('gal').setAttribute('cx', 90 + (v / 60) * 530);

  var visible = v <= SEE;
  document.getElementById('reachTxt').textContent =
    v <= REACH ? 'Yes, in principle' : visible ? 'No, never' : 'We cannot even see it';
  document.getElementById('gal').setAttribute('opacity', visible ? 1 : .25);

  document.getElementById('seeTxt').textContent = visible
    ? 'ITS LIGHT HAS REACHED US'
    : 'ITS LIGHT HAS NOT ARRIVED AND MAY NEVER ARRIVE';
  document.getElementById('ageTxt').textContent = visible
    ? 'YOU ARE SEEING IT AS IT WAS, LONG AGO'
    : '';
}
d.addEventListener('input', draw);
draw();
''',
   'caption': 'Push the galaxy outward. Somewhere past 16 billion light years it stops '
              'being reachable — we can watch it, but nothing we ever send will catch '
              'up with it.'},

  {'type': 'scene', 'tone': 'ember', 'scene': 'expand',
   'h': 'And the reachable part is shrinking',
   'p': 'Expansion is speeding up. Every year, a few more galaxies drift permanently '
        'out of range. The universe we could ever touch is quietly getting smaller.'},
 ],

 'zoomout': {'tone': 'nebula',
   'text': 'We arrived early enough to see it. Anyone looking up in a hundred billion '
           'years will see an empty sky and have no way of knowing there was ever '
           'anything else. Being able to ask this question is itself a piece of luck.'},
},

# ================================================================== 03
{
 'slug': 'are-we-alone',
 'kicker': 'Life',
 'card_tone': 'forest', 'card_scene': 'stars',
 'featured': True,
 'title': 'If the universe is so big, where is everybody?',
 'teaser': 'Hundreds of billions of stars in our galaxy alone. Billions of years of time. And silence.',
 'hero': {'tone': 'forest', 'scene': 'stars',
   'standfirst': 'Our galaxy has been around long enough for a civilisation to cross '
                 'it many times over. By every reasonable estimate, someone should '
                 'have arrived by now. Nobody has.'},

 'blocks': [
  {'type': 'text', 'h': 'The numbers are absurd in our favour',
   'p': ['Our galaxy holds a few hundred billion stars. Most have planets. Many of '
         'those planets sit at a comfortable distance from their star.',
         'And the galaxy is old. If even one species had started spreading a million '
         'years ago, they would already be <strong>everywhere</strong>.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'dying',
   'h': 'So the sky should be busy. It is not.',
   'p': 'No signals. No probes. No evidence of anything, anywhere, ever. That gap '
        'between what we expect and what we find is the whole problem.'},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'Something stops civilisations from filling the galaxy. We do not know what, or whether we have passed it yet.'},

  {'type': 'steps', 'tone': 'solar', 'h': 'Where the barrier could be',
   'items': [
     {'h': 'Behind us', 'p': 'Starting life at all may be a fluke so rare it has happened once. If so, we are alone, and we are safe.'},
     {'h': 'Also behind us', 'p': 'Simple cells took billions of years to become complex ones. That step may almost never happen.'},
     {'h': 'Ahead of us', 'p': 'Every civilisation might destroy itself shortly after learning how. This is the version worth worrying about.'}]},

  {'type': 'figure', 'tone': 'forest',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How many civilisations should be out there right now</title>
  <g id="dots"></g>
  <text class="f-label" x="20" y="230">CIVILISATIONS TALKING RIGHT NOW, IN OUR GALAXY</text>
  <text class="f-value" id="nTxt" x="20" y="272" style="font-size:34px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="life">Planets that get life</label>
  <input type="range" id="life" min="0" max="100" step="1" value="30">
  <span class="readout" id="lifeOut">&#8212;</span>
</div>
<div class="control">
  <label for="last">How long they last</label>
  <input type="range" id="last" min="0" max="100" step="1" value="30">
  <span class="readout" id="lastOut">&#8212;</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var life = document.getElementById('life'), last = document.getElementById('last');
var dots = document.getElementById('dots'), nodes = [];
for (var i = 0; i < 120; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 24 + (i % 30) * 21);
  c.setAttribute('cy', 50 + ((i / 30) | 0) * 42);
  c.setAttribute('r', 6);
  dots.appendChild(c);
  nodes.push(c);
}

function draw() {
  // a deliberately crude Drake-style estimate: stars with planets, times the
  // fraction that get life, times how long a civilisation stays detectable
  var STARS = 100e9, HAB = 0.2;
  var fLife = Math.pow(+life.value / 100, 3);       // life is the brutal filter
  var fLast = Math.pow(+last.value / 100, 2);
  var n = STARS * HAB * fLife * fLast * 1e-5;

  document.getElementById('lifeOut').textContent =
    (+life.value < 10 ? 'almost none' : +life.value > 80 ? 'most of them' : life.value + '%');
  document.getElementById('lastOut').textContent =
    (+last.value < 10 ? 'a blink' : +last.value > 80 ? 'forever' : last.value + '%');

  document.getElementById('nTxt').textContent =
    n < 1 ? 'probably just us' :
    n > 1e6 ? Math.round(n).toExponential(1).replace('e+', ' x 10^') :
    Math.round(n).toLocaleString('en-GB');

  var lit = Math.max(0, Math.min(120, Math.round(Math.log10(Math.max(n, 1)) * 20)));
  nodes.forEach(function (d, i) {
    d.setAttribute('fill', i < lit ? '#fff' : 'rgba(255,255,255,.16)');
  });
}
life.addEventListener('input', draw);
last.addEventListener('input', draw);
draw();
''',
   'caption': 'Nobody knows either number. That is the honest answer — slide them a '
              'little and the result swings from an empty galaxy to a crowded one, '
              'which is exactly why the question is still open.'},

  {'type': 'text', 'h': 'Silence is not comforting',
   'p': ['If we ever find simple life on Mars or under the ice of Europa, that means '
         'life is easy — and the hard step is probably still <strong>in front of us</strong>.',
         'The best news would be finding nothing at all. An empty galaxy might mean we '
         'already got through the difficult part.']},
 ],

 'zoomout': {'tone': 'forest',
   'text': 'Either we are alone in an unimaginably large place, or we are not. Both '
           'answers are enormous, and we are the first generation with instruments '
           'good enough to start ruling one of them out.'},
},

# ================================================================== 04
{
 'slug': 'mostly-empty-space',
 'kicker': 'Matter',
 'card_tone': 'deepsea', 'card_scene': 'atom',
 'featured': True,
 'title': 'You are almost entirely empty space',
 'teaser': 'If atoms are mostly nothing, why does the floor hold you up?',
 'hero': {'tone': 'deepsea', 'scene': 'atom',
   'standfirst': 'Everything you have ever touched is more than 99.999% empty. So is '
                 'your hand. Somehow the two of them still refuse to pass through '
                 'each other.'},

 'blocks': [
  {'type': 'text', 'h': 'An atom is nearly all gap',
   'p': ['Almost all of an atom\'s weight sits in a nucleus at the centre. Around it, '
         'a long way out, are the electrons.',
         'Blow an atom up so the nucleus is a marble on a football pitch. The nearest '
         'electron is <strong>somewhere in the stands</strong>. Between them: nothing.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'atom',
   'h': 'A marble in a stadium',
   'p': 'That is the actual ratio. Every solid thing you know is built out of this.'},

  {'type': 'turn', 'tone': 'ember',
   'text': 'Nothing ever really touches anything. You have never made contact with a single object in your life.'},

  {'type': 'text', 'h': 'So what stops your hand going through the table?',
   'p': ['Two things, and neither of them is solidity. First, electrons repel other '
         'electrons — same charge, pushing apart, harder the closer they get.',
         'Second, and stranger: electrons flatly <strong>refuse to share a state</strong>. '
         'Squeeze them together and they push back, not because of a force, but '
         'because the universe will not allow the arrangement.']},

  {'type': 'figure', 'tone': 'deepsea',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">The size of a nucleus compared with its atom</title>
  <circle id="shell" cx="200" cy="150" r="120" fill="none" stroke="rgba(255,255,255,.35)" stroke-dasharray="5 6"/>
  <circle id="nuc" cx="200" cy="150" r="3" fill="#fff"/>
  <text class="f-label" x="200" y="290" text-anchor="middle">THE WHOLE ATOM</text>
  <text class="f-label" x="400" y="70">IF THE NUCLEUS WERE</text>
  <text class="f-value" id="objTxt" x="400" y="104" style="font-size:24px">&#8212;</text>
  <text class="f-label" x="400" y="152">THE ATOM WOULD BE</text>
  <text class="f-value" id="scaleTxt" x="400" y="186" style="font-size:24px">&#8212;</text>
  <text class="f-label" x="400" y="234">EMPTY SPACE INSIDE YOU</text>
  <text class="f-value" id="emptyTxt" x="400" y="266" style="font-size:20px">99.9999999999999%</text>
</svg>''',
   'controls': '''<div class="chips" role="group" aria-label="Pick something to compare">
  <button class="chip" id="oMarble" aria-pressed="true">A marble</button>
  <button class="chip" id="oPea" aria-pressed="false">A pea</button>
  <button class="chip" id="oBall" aria-pressed="false">A football</button>
</div>''',
   'js': '''
// a nucleus is roughly 1/100,000 the width of its atom
var OBJ = {
  oMarble: { name: 'a marble (1 cm)',   out: 'about 1 km wide' },
  oPea:    { name: 'a pea (5 mm)',      out: 'about 500 m wide' },
  oBall:   { name: 'a football (22 cm)', out: 'about 22 km wide' }
};

function show(key) {
  Object.keys(OBJ).forEach(function (k) {
    document.getElementById(k).setAttribute('aria-pressed', k === key ? 'true' : 'false');
  });
  document.getElementById('objTxt').textContent = OBJ[key].name;
  document.getElementById('scaleTxt').textContent = OBJ[key].out;
}
Object.keys(OBJ).forEach(function (k) {
  document.getElementById(k).addEventListener('click', function () { show(k); });
});

// gently breathe the shell so the emptiness reads as a volume, not a ring
var shell = document.getElementById('shell'), t0 = null;
function tick(ts) {
  if (t0 === null) t0 = ts;
  var s = 120 + Math.sin((ts - t0) / 1400) * 6;
  shell.setAttribute('r', s);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
show('oMarble');
''',
   'caption': 'The white dot in the middle is drawn far too big to be honest. At the '
              'real ratio it would be smaller than one pixel on your screen.'},

  {'type': 'scene', 'tone': 'rose', 'scene': 'grid',
   'h': 'Solidity is a feeling, not a fact',
   'p': 'What you call touching is the push of one electron cloud against another, '
        'reported to your brain as a surface.'},
 ],

 'zoomout': {'tone': 'deepsea',
   'text': 'You are a very thin arrangement of almost nothing, held apart from all the '
           'other almost-nothing by rules rather than by substance. And it holds. It '
           'has held every second of your life.'},
},

# ================================================================== 05
{
 'slug': 'the-war-inside-you',
 'kicker': 'Your body',
 'card_tone': 'ember', 'card_scene': 'cells',
 'featured': False,
 'title': 'There is a war going on inside you right now',
 'teaser': 'Millions of things are trying to get in. Something is stopping them, and you never notice.',
 'hero': {'tone': 'ember', 'scene': 'cells',
   'standfirst': 'While you read this, something inside you is finding, identifying '
                 'and killing invaders — thousands of them — and you will not feel a '
                 'single one of those fights.'},

 'blocks': [
  {'type': 'text', 'h': 'It starts with a cut',
   'p': ['Break the skin and the outer wall is down. Bacteria that were sitting '
         'harmlessly on the surface are suddenly inside, in warm wet tissue, and they '
         'start doubling.',
         'Within seconds, something has already noticed.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'cells',
   'h': 'First the ones that just eat',
   'p': 'Big, blunt cells arrive and swallow anything that does not have the right '
        'password. No thinking, no targeting. Just eating.'},

  {'type': 'steps', 'tone': 'solar', 'h': 'What the swelling actually is',
   'items': [
     {'h': 'Blood vessels open up', 'p': 'More blood to the area means more defenders arriving. That is the redness and the heat.'},
     {'h': 'The walls get leaky', 'p': 'Fluid floods in so cells can move through the tissue. That is the puffiness.'},
     {'h': 'Nerves get sensitive', 'p': 'It hurts so you protect the spot. The pain is a design decision, not a malfunction.'}]},

  {'type': 'turn', 'tone': 'rose',
   'text': 'Every symptom you hate is your own body fighting. The infection barely does anything to you. Winning is what feels awful.'},

  {'type': 'text', 'h': 'Then the specialists show up',
   'p': ['If the blunt cells cannot finish it, they carry a piece of the enemy back and '
         'show it around until they find the one cell that recognises it.',
         'That cell then copies itself furiously, building an army <strong>shaped for '
         'this specific invader</strong>. It takes days. That is why you stay ill for '
         'a week.']},

  {'type': 'figure', 'tone': 'ember',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Invaders and defenders over the days after a cut</title>
  <line class="f-faint" x1="40" y1="230" x2="630" y2="230"/>
  <path id="germLine" class="f-line" d="" stroke="rgba(255,255,255,.55)" stroke-dasharray="6 5"/>
  <path id="immLine" class="f-line" d=""/>
  <line id="cursor" class="f-faint" x1="40" y1="40" x2="40" y2="230"/>
  <text class="f-label" x="40" y="252">THE CUT</text>
  <text class="f-label" x="630" y="252" text-anchor="end">DAY 10</text>
  <text class="f-label" x="40" y="40">INVADERS (DASHED) &#183; DEFENDERS (SOLID)</text>
  <text class="f-value" id="stateTxt" x="40" y="288" style="font-size:19px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="day">Days since the cut</label>
  <input type="range" id="day" min="0" max="100" step="1" value="0">
  <span class="readout" id="dayOut">0.0</span>
</div>''',
   'js': '''
var day = document.getElementById('day');

function germs(t) {           // explode, then get crushed once the specialists arrive
  return Math.max(0, Math.exp(-Math.pow((t - 2.2) / 1.9, 2)) * 0.95 - (t > 5 ? (t - 5) * 0.08 : 0));
}
function immune(t) {          // slow to start, then overwhelming
  return Math.min(1, 0.08 + Math.pow(t / 10, 1.5) * 1.25);
}

function path(fn) {
  var d = '';
  for (var i = 0; i <= 100; i++) {
    var t = i / 10;
    var x = 40 + (i / 100) * 590;
    var y = 230 - fn(t) * 175;
    d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1);
  }
  return d;
}
document.getElementById('germLine').setAttribute('d', path(germs));
document.getElementById('immLine').setAttribute('d', path(immune));

function draw() {
  var t = +day.value / 10;
  document.getElementById('dayOut').textContent = t.toFixed(1);
  document.getElementById('cursor').setAttribute('x1', 40 + (+day.value / 100) * 590);
  document.getElementById('cursor').setAttribute('x2', 40 + (+day.value / 100) * 590);
  document.getElementById('stateTxt').textContent =
    t < 0.5 ? 'The wall is broken. Nothing has arrived yet.' :
    t < 2   ? 'The eaters are here. You feel warm and sore.' :
    t < 4   ? 'Losing ground. This is when you feel worst.' :
    t < 7   ? 'The specialists arrive. The tide turns.' :
              'Almost over. Some of those cells will remember this forever.';
}
day.addEventListener('input', draw);
draw();
''',
   'caption': 'Drag through the days. You feel worst around day two or three — not '
              'when the invaders are winning, but when your own response is at full '
              'volume.'},

  {'type': 'scene', 'tone': 'forest', 'scene': 'cells',
   'h': 'And then it remembers',
   'p': 'A few of those specialist cells stay behind for decades. Meet the same '
        'invader again and the fight is over before you notice it started. That is '
        'what immunity is, and what a vaccine borrows.'},
 ],

 'zoomout': {'tone': 'ember',
   'text': 'You have never had to think about any of this. Not once. Something inside '
           'you has been making life-or-death identifications every second since the '
           'day you were born, and it has never asked you for anything.'},
},

# ================================================================== 06
{
 'slug': 'are-you-the-same-person',
 'kicker': 'Mind',
 'card_tone': 'rose', 'card_scene': 'replace',
 'featured': False,
 'title': 'Are you the same person you were ten years ago?',
 'teaser': 'Almost every piece of you has been swapped out. So what exactly kept going?',
 'hero': {'tone': 'rose', 'scene': 'replace',
   'standfirst': 'The atoms that made you a decade ago are mostly gone — eaten, '
                 'breathed out, worn away. Something is still here calling itself you. '
                 'The question is what.'},

 'blocks': [
  {'type': 'text', 'h': 'You are a pattern, not a substance',
   'p': ['Your skin is weeks old. Your gut lining is days old. Even your bones swap '
         'themselves out over about ten years.',
         'You are less like a statue and more like <strong>a wave</strong> — the water '
         'keeps changing, the shape keeps going.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'replace',
   'h': 'Swap every plank on a ship, one at a time',
   'p': 'At what point does it stop being the same ship? People have argued about this '
        'for two thousand years and never settled it.'},

  {'type': 'text', 'h': 'Not everything gets replaced',
   'p': ['A few parts stay. Most of the neurons in your brain are as old as you are, '
         'and never get swapped.',
         'The lens in your eye is original too. So is some of the enamel on your '
         'teeth. There is a thin thread of <em>original you</em> running through it.']},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'What continues is not the stuff. It is the arrangement, copying itself forward, slightly imperfectly, every single day.'},

  {'type': 'figure', 'tone': 'rose',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How much of your body has been replaced over time</title>
  <g id="body"></g>
  <text class="f-label" x="360" y="70">REPLACED BY NOW</text>
  <text class="f-value" id="pctTxt" x="360" y="108" style="font-size:32px">&#8212;</text>
  <text class="f-label" x="360" y="158">STILL THE ORIGINAL</text>
  <text class="f-value" id="keepTxt" x="360" y="192" style="font-size:20px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="360" y="244">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="yrs">Years that have passed</label>
  <input type="range" id="yrs" min="0" max="30" step="1" value="10">
  <span class="readout" id="yrsOut">10 years</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var yrs = document.getElementById('yrs');
var body = document.getElementById('body'), cells = [];
for (var i = 0; i < 96; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 30 + (i % 12) * 24);
  c.setAttribute('cy', 50 + ((i / 12) | 0) * 26);
  c.setAttribute('r', 8);
  body.appendChild(c);
  cells.push(c);
}

function draw() {
  var y = +yrs.value;
  document.getElementById('yrsOut').textContent = y + (y === 1 ? ' year' : ' years');
  // most tissue turns over within a decade; a fixed remainder never does
  var swapped = Math.min(0.9, 1 - Math.exp(-y / 4.2));
  document.getElementById('pctTxt').textContent = Math.round(swapped * 100) + '%';
  document.getElementById('keepTxt').textContent = 'brain, eye lens, tooth enamel';
  document.getElementById('noteTxt').textContent =
    y === 0 ? 'NOTHING HAS CHANGED YET' :
    y < 5   ? 'SKIN, BLOOD AND GUT ARE NEW' :
    y < 15  ? 'YOUR SKELETON HAS TURNED OVER' :
              'ALMOST ALL OF IT REPLACED';
  cells.forEach(function (c, i) {
    var isNew = i / cells.length < swapped;
    c.setAttribute('fill', isNew ? '#fff' : 'rgba(255,255,255,.2)');
  });
}
yrs.addEventListener('input', draw);
draw();
''',
   'caption': 'Filled circles have been replaced. Drag far enough and nearly all of '
              'them fill in — and you still have every memory you started with.'},

  {'type': 'scene', 'tone': 'solar', 'scene': 'bloom',
   'h': 'Your memories are not recordings',
   'p': 'Every time you remember something you rebuild it, and save the rebuilt copy. '
        'A memory you revisit often is the one furthest from what happened.'},
 ],

 'zoomout': {'tone': 'rose',
   'text': 'You are not a thing that persists. You are a process that keeps happening, '
           'made of borrowed material, holding its shape long enough to wonder whether '
           'it is still itself.'},
},

# ================================================================== 07
{
 'slug': 'if-the-sun-vanished',
 'kicker': 'Space',
 'card_tone': 'solar', 'card_scene': 'beam',
 'featured': False,
 'title': 'What if the Sun vanished right now?',
 'teaser': 'For eight minutes, nothing would happen. Not the light, and not the gravity either.',
 'hero': {'tone': 'solar', 'scene': 'beam',
   'standfirst': 'Suppose the Sun simply stopped existing this second. The surprise is '
                 'not what happens. It is how long absolutely nothing happens for.'},

 'blocks': [
  {'type': 'text', 'h': 'The light is old news',
   'p': ['Sunlight takes about eight minutes and twenty seconds to cross the gap to '
         'Earth. The light already in flight keeps coming.',
         'For eight minutes the sky stays bright, the day stays warm, and nobody on '
         'Earth has any way of knowing.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'beam',
   'h': 'Gravity is not instant either',
   'p': 'This is the part that trips people up. Gravity travels at exactly the same '
        'speed as light. Not faster. Not instantly.'},

  {'type': 'turn', 'tone': 'ember',
   'text': 'Earth would keep circling a Sun that was not there — for the same eight minutes, to the second.'},

  {'type': 'text', 'h': 'Then both arrive together',
   'p': ['At eight minutes twenty, the sky goes dark and Earth stops turning its '
         'corner at the same instant.',
         'We would not fly outward, exactly. We would go <strong>straight</strong> — '
         'off along whatever direction we happened to be travelling, in a line, forever.']},

  {'type': 'figure', 'tone': 'solar',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What Earth experiences in the minutes after the Sun disappears</title>
  <circle id="sun" cx="150" cy="150" r="42" fill="#FFD36E"/>
  <path id="orbit" class="f-faint" d="M150 150 m -110 0 a 110 110 0 1 0 220 0 a 110 110 0 1 0 -220 0"/>
  <path id="escape" class="f-line" d="" stroke-dasharray="6 6" opacity="0"/>
  <circle id="earth" cx="260" cy="150" r="10" fill="#7FC7FF"/>
  <text class="f-label" x="400" y="70">ON EARTH IT IS</text>
  <text class="f-value" id="skyTxt" x="400" y="106" style="font-size:24px">&#8212;</text>
  <text class="f-label" x="400" y="156">EARTH IS</text>
  <text class="f-value" id="moveTxt" x="400" y="192" style="font-size:20px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="400" y="244">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="min">Minutes since the Sun vanished</label>
  <input type="range" id="min" min="0" max="200" step="1" value="0">
  <span class="readout" id="minOut">0:00</span>
</div>''',
   'js': '''
var min = document.getElementById('min');
var DELAY = 8.32;   // minutes for light, and for gravity, to cross the gap

function draw() {
  var m = +min.value / 10;
  var mm = Math.floor(m), ss = Math.round((m - mm) * 60);
  document.getElementById('minOut').textContent = mm + ':' + (ss < 10 ? '0' : '') + ss;

  var before = m < DELAY;
  document.getElementById('sun').setAttribute('opacity', before ? 1 : 0);
  document.getElementById('skyTxt').textContent = before ? 'a perfectly normal day' : 'dark, and getting cold';
  document.getElementById('moveTxt').textContent = before ? 'still curving in its orbit' : 'travelling in a straight line';
  document.getElementById('noteTxt').textContent = before
    ? 'NOBODY KNOWS YET'
    : 'LIGHT AND PULL STOPPED TOGETHER';

  if (before) {
    var a = -m * 0.5;
    document.getElementById('earth').setAttribute('cx', 150 + Math.cos(a) * 110);
    document.getElementById('earth').setAttribute('cy', 150 + Math.sin(a) * 110);
    document.getElementById('escape').setAttribute('opacity', 0);
    document.getElementById('orbit').setAttribute('opacity', 1);
  } else {
    // released on a tangent at the moment the news arrived
    var a0 = -DELAY * 0.5;
    var x0 = 150 + Math.cos(a0) * 110, y0 = 150 + Math.sin(a0) * 110;
    var tx = -Math.sin(a0), ty = Math.cos(a0);
    var d = (m - DELAY) * 26;
    document.getElementById('earth').setAttribute('cx', x0 + tx * d);
    document.getElementById('earth').setAttribute('cy', y0 + ty * d);
    document.getElementById('escape').setAttribute('d',
      'M' + x0 + ' ' + y0 + ' L' + (x0 + tx * 300) + ' ' + (y0 + ty * 300));
    document.getElementById('escape').setAttribute('opacity', .8);
    document.getElementById('orbit').setAttribute('opacity', .25);
  }
}
min.addEventListener('input', draw);
draw();
''',
   'caption': 'Nothing at all happens until 8:20. Then everything happens at once — '
              'and Earth leaves along a straight line, not outward from where the Sun '
              'used to be.'},

  {'type': 'scene', 'tone': 'deepsea', 'scene': 'grid',
   'h': 'Why gravity has a speed at all',
   'p': 'Gravity is not a rope pulling you. It is a dent in space, and a dent has to '
        'spread outward like a ripple. Remove the weight and the ripple takes time to '
        'arrive.'},
 ],

 'zoomout': {'tone': 'solar',
   'text': 'Nothing in the universe finds out about anything instantly. Every fact has '
           'to travel, and none of it travels faster than light. The present moment is '
           'strictly local, and everything else is news.'},
},

# ================================================================== 08
{
 'slug': 'how-the-universe-ends',
 'kicker': 'Time',
 'card_tone': 'void', 'card_scene': 'dying',
 'featured': False,
 'title': 'How does the universe end?',
 'teaser': 'Not with a bang. With a very, very long dimming.',
 'hero': {'tone': 'void', 'scene': 'dying',
   'standfirst': 'The universe is 13.8 billion years old, which sounds ancient. On the '
                 'timeline of how long it has left, it has barely started.'},

 'blocks': [
  {'type': 'text', 'h': 'Stars are a phase, not a feature',
   'p': ['Stars need gas to form from, and every star burns some of it permanently '
         'into heavier stuff.',
         'There is a fixed budget. In about a hundred trillion years the last star '
         'will form, burn, and go out. <strong>After that, no new ones. Ever.</strong>']},

  {'type': 'scene', 'tone': 'dusk', 'scene': 'dying',
   'h': 'The lights go out one at a time',
   'p': 'The small red ones last longest. The last of them will still be glowing '
        'faintly a thousand times longer than the universe has existed so far.'},

  {'type': 'steps', 'tone': 'nebula', 'h': 'What comes after the lights',
   'items': [
     {'h': 'The dark era', 'p': 'Cold leftovers drifting: dead stars, dead planets, black holes. Nothing shines.'},
     {'h': 'The black holes eat', 'p': 'They pull in what is left and become the only structures of any size in the universe.'},
     {'h': 'The black holes leak', 'p': 'Even they evaporate, unbelievably slowly. The largest take longer than any number worth writing down.'}]},

  {'type': 'turn', 'tone': 'ember',
   'text': 'Everything ends the same way: spread out, cooled down, and too even for anything to happen.'},

  {'type': 'figure', 'tone': 'void',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What still exists at different points in the far future</title>
  <g id="sky"></g>
  <line class="f-faint" x1="30" y1="200" x2="630" y2="200"/>
  <circle id="mark" cx="30" cy="200" r="6" fill="#fff"/>
  <text class="f-label" x="30" y="222">NOW</text>
  <text class="f-label" x="630" y="222" text-anchor="end">10^100 YEARS</text>
  <text class="f-label" x="30" y="256">WHAT IS LEFT</text>
  <text class="f-value" id="eraTxt" x="30" y="288" style="font-size:22px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="pow">Years from now</label>
  <input type="range" id="pow" min="0" max="100" step="1" value="1">
  <span class="readout" id="powOut">&#8212;</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var pow = document.getElementById('pow');
var sky = document.getElementById('sky'), stars = [];
for (var i = 0; i < 90; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 30 + Math.random() * 600);
  c.setAttribute('cy', 30 + Math.random() * 140);
  c.setAttribute('r', 1 + Math.random() * 2.4);
  c.setAttribute('fill', '#fff');
  sky.appendChild(c);
  stars.push(c);
}

function draw() {
  var p = +pow.value;                       // exponent: 10^p years from now
  document.getElementById('powOut').textContent =
    p < 1 ? 'today' : '10^' + p + ' years';
  document.getElementById('mark').setAttribute('cx', 30 + (p / 100) * 600);

  var era, lit;
  if (p < 10)      { era = 'Stars, planets, and us';            lit = 1; }
  else if (p < 14) { era = 'The last stars are forming';        lit = .55; }
  else if (p < 15) { era = 'The final stars burn out';          lit = .12; }
  else if (p < 40) { era = 'Cold dead remnants, drifting';      lit = .02; }
  else if (p < 67) { era = 'Only black holes remain';           lit = .008; }
  else if (p < 100){ era = 'Even the black holes are leaking';  lit = .004; }
  else             { era = 'Nothing but thin, even, cold light'; lit = 0; }

  document.getElementById('eraTxt').textContent = era;
  stars.forEach(function (s, i) {
    s.setAttribute('opacity', i / stars.length < lit ? .9 : 0);
  });
}
pow.addEventListener('input', draw);
draw();
''',
   'caption': 'Each step on this slider multiplies the time by ten. Almost the entire '
              'history of stars — including every one you have ever seen — happens in '
              'the first sliver on the left.'},

  {'type': 'text', 'h': 'This is not a sad story yet',
   'p': ['We are in the brightest, busiest, most eventful slice the universe will ever '
         'have. Stars are burning, planets are forming, chemistry is happening.',
         'By any measure of time, we turned up <strong>at the beginning</strong>, while '
         'the lights were still on.']},
 ],

 'zoomout': {'tone': 'void',
   'text': 'Everything ends. It just takes so long that the ending is not really the '
           'point. The point is that for one brief, absurdly early moment there was '
           'enough going on for something to sit up and notice.'},
},

# ================================================================== 09
{
 'slug': 'why-is-there-anything',
 'kicker': 'Matter',
 'card_tone': 'nebula', 'card_scene': 'flicker',
 'featured': False,
 'title': 'Why is there something instead of nothing?',
 'teaser': 'Empty space is not empty. It cannot be. The rules do not allow it.',
 'hero': {'tone': 'nebula', 'scene': 'flicker',
   'standfirst': 'Take a box. Remove all the air, all the light, all the heat, every '
                 'last particle. What is left is still not nothing — and that turns '
                 'out to be one of the deepest facts we know.'},

 'blocks': [
  {'type': 'text', 'h': 'Perfect emptiness is forbidden',
   'p': ['To be truly empty, a patch of space would have to hold exactly zero energy '
         'and stay exactly that way.',
         'The rules of the very small do not permit anything to be that precisely '
         'pinned down. So <strong>space fidgets</strong>.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'flicker',
   'h': 'Pairs appear and cancel out constantly',
   'p': 'A particle and its opposite, borrowed from nothing, gone again before the '
        'universe notices the debt. Everywhere. Always.'},

  {'type': 'text', 'h': 'We can measure it',
   'p': ['Put two metal plates extremely close together in a vacuum and they get '
         'pushed together by the fidgeting outside them.',
         'That push has been measured. Empty space is doing something, and it is '
         'strong enough to move objects.']},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'Nothing may simply be an unstable state. Given the rules we have, something is what you get by default.'},

  {'type': 'figure', 'tone': 'nebula',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Looking into an apparently empty box at increasing magnification</title>
  <rect x="40" y="40" width="360" height="220" rx="16" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.4)"/>
  <g id="pairs"></g>
  <text class="f-label" x="440" y="80">THE BOX IS</text>
  <text class="f-value" id="stateTxt" x="440" y="114" style="font-size:22px">empty</text>
  <text class="f-label" x="440" y="164">PAIRS RIGHT NOW</text>
  <text class="f-value" id="cntTxt" x="440" y="198" style="font-size:26px">0</text>
  <text class="f-label" id="hintTxt" x="440" y="246">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="zoom">Look closer</label>
  <input type="range" id="zoom" min="0" max="100" step="1" value="0">
  <span class="readout" id="zoomOut">normal eyes</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var zoom = document.getElementById('zoom');
var host = document.getElementById('pairs'), pairs = [];
for (var i = 0; i < 40; i++) {
  var g = document.createElementNS(NS, 'g');
  var x = 60 + Math.random() * 320, y = 60 + Math.random() * 180;
  g.innerHTML = '<circle cx="' + x + '" cy="' + y + '" r="3.5" fill="#fff"/>' +
                '<circle cx="' + x + '" cy="' + y + '" r="3.5" fill="rgba(255,255,255,.45)"/>';
  host.appendChild(g);
  pairs.push({ g: g, a: g.children[0], b: g.children[1], x: x, y: y, ph: Math.random() * 6.28 });
}

var level = 0;
function draw() {
  level = +zoom.value / 100;
  document.getElementById('zoomOut').textContent =
    level < .2 ? 'normal eyes' : level < .5 ? 'a good microscope' :
    level < .8 ? 'far beyond any microscope' : 'the smallest scale there is';
  document.getElementById('stateTxt').textContent =
    level < .2 ? 'empty' : level < .5 ? 'still looks empty' : 'boiling';
  document.getElementById('hintTxt').textContent =
    level < .5 ? 'NOTHING TO SEE, APPARENTLY' : 'BORROWED AND PAID BACK';
}

var t0 = null;
function tick(ts) {
  if (t0 === null) t0 = ts;
  var t = (ts - t0) / 1000;
  var shown = 0;
  pairs.forEach(function (p, i) {
    if (i / pairs.length > level) { p.g.setAttribute('opacity', 0); return; }
    var f = ((t * 0.8 + p.ph) % 2) / 2;
    if (f > .5) { p.g.setAttribute('opacity', 0); return; }
    var k = Math.sin(f * 2 * Math.PI);
    p.g.setAttribute('opacity', Math.abs(k));
    p.a.setAttribute('cx', p.x - k * 9);
    p.b.setAttribute('cx', p.x + k * 9);
    shown++;
  });
  document.getElementById('cntTxt').textContent = shown;
  requestAnimationFrame(tick);
}
zoom.addEventListener('input', draw);
requestAnimationFrame(tick);
draw();
''',
   'caption': 'Nothing changes in the box as you look closer. The box was always doing '
              'this — you were simply never able to resolve it.'},

  {'type': 'scene', 'tone': 'rose', 'scene': 'flicker',
   'h': 'It does not finish the job',
   'p': 'This tells us why there is not nothing. It still does not tell us where the '
        'rules came from. That question is entirely open, and may stay that way.'},
 ],

 'zoomout': {'tone': 'nebula',
   'text': 'We have moved the mystery rather than solved it. But moving it was real '
           'progress: "why is there anything" turned out to have a physical answer, '
           'and the leftover question is now sharper than the one we started with.'},
},

# ================================================================== 10
{
 'slug': 'what-light-experiences',
 'kicker': 'Light',
 'card_tone': 'solar', 'card_scene': 'beam',
 'featured': False,
 'title': 'For light, no time passes at all',
 'teaser': 'A photon from the edge of the universe travelled 13 billion years. From its side, it arrived instantly.',
 'hero': {'tone': 'solar', 'scene': 'beam',
   'standfirst': 'Go faster and your clock slows down. Everyone knows that bit. What '
                 'is less well known is what happens when you reach the top speed — '
                 'because the clock does not slow. It stops.'},

 'blocks': [
  {'type': 'text', 'h': 'Speed borrows from time',
   'p': ['Everything is always moving through space and through time together, and '
         'there is a fixed budget shared between them.',
         'Stand still and all of it goes into time. Move fast and you spend some of it '
         'on space, so <strong>less is left for the clock</strong>.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'beam',
   'h': 'Light spends the whole budget on motion',
   'p': 'Nothing is left over. Its clock does not run slowly — it does not run.'},

  {'type': 'turn', 'tone': 'nebula',
   'text': 'A photon that crossed the entire universe was emitted and absorbed in the same instant, as far as it is concerned.'},

  {'type': 'figure', 'tone': 'solar',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How much time passes for a traveller at different speeds</title>
  <line class="f-faint" x1="40" y1="120" x2="620" y2="120"/>
  <circle id="ship" cx="40" cy="120" r="11" fill="#fff"/>
  <text class="f-label" x="40" y="96">YOU SET OFF</text>
  <text class="f-label" x="620" y="96" text-anchor="end">10 LIGHT YEARS LATER</text>
  <text class="f-label" x="40" y="184">TIME PASSING ON EARTH</text>
  <text class="f-value" id="earthTxt" x="40" y="218" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="360" y="184">TIME PASSING FOR YOU</text>
  <text class="f-value" id="youTxt" x="360" y="218" style="font-size:26px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="40" y="268">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="v">Your speed</label>
  <input type="range" id="v" min="0" max="99999" step="1" value="50000">
  <span class="readout" id="vOut">&#8212;</span>
</div>''',
   'js': '''
var v = document.getElementById('v');

function draw() {
  var beta = +v.value / 100000;              // fraction of the speed of light
  document.getElementById('vOut').textContent = (beta * 100).toFixed(3) + '% of light';
  document.getElementById('ship').setAttribute('cx', 40 + beta * 580);

  var earth = 10 / Math.max(beta, 1e-5);     // years, from Earth's point of view
  var you = earth * Math.sqrt(1 - beta * beta);

  document.getElementById('earthTxt').textContent =
    earth > 9999 ? 'a very long time' : earth.toFixed(1) + ' years';
  document.getElementById('youTxt').textContent =
    you < 0.02 ? 'almost none' : you.toFixed(2) + ' years';
  document.getElementById('noteTxt').textContent =
    beta > 0.9999 ? 'AT EXACTLY LIGHT SPEED, THE TRIP TAKES YOU NO TIME AT ALL'
    : beta > 0.99 ? 'THE JOURNEY IS BARELY LASTING FOR YOU'
    : 'BOTH CLOCKS STILL ROUGHLY AGREE';
}
v.addEventListener('input', draw);
draw();
''',
   'caption': 'Push the speed to the far right. Earth\'s clock keeps ticking through '
              'the whole trip while yours very nearly stops — and light sits just past '
              'the end of this slider, where it stops completely.'},

  {'type': 'text', 'h': 'This is why the speed limit exists',
   'p': ['It is not that we lack a fast enough engine. At light speed there is no time '
         'left to experience, so there is nothing further to go.',
         'The limit is not a wall in front of you. It is the <strong>edge of what '
         'moving even means</strong>.']},

  {'type': 'scene', 'tone': 'deepsea', 'scene': 'stars',
   'h': 'Every star you see reached you instantly',
   'p': 'From your side, that light is thousands of years old. From its side, it left '
        'and arrived in the same moment. Both are completely true.'},
 ],

 'zoomout': {'tone': 'solar',
   'text': 'Time is not a stage everything sits on. It is something each thing has its '
           'own supply of, spent at its own rate — and light, moving as fast as '
           'anything can, has none to spend at all.'},
},

]

# The second shelf lives in its own file; build.py only ever sees one list.
from stories_more import MORE  # noqa: E402
STORIES = STORIES + MORE
