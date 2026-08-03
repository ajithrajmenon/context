# -*- coding: utf-8 -*-
"""The second shelf of stories.

Same shape as stories_data.py — see the docstring there. Split only because
one file of twenty was getting unwieldy; stories_data imports this and
concatenates, so build.py and everything downstream sees a single list.

These lean human rather than mechanical: bodies, minds, populations, the
sea, the things people already wonder about on their own.
"""

MORE = [

# ================================================================== 11
{
 'slug': 'what-happens-when-you-die',
 'kicker': 'Your body',
 'card_tone': 'void', 'card_scene': 'pulse',
 'featured': True,
 'title': 'What actually happens when you die?',
 'teaser': 'Not a switch flicking off. A shutdown that runs in a specific order and takes hours.',
 'hero': {'tone': 'void', 'scene': 'pulse',
   'standfirst': 'We talk about death as a moment — a line you cross. Biologically '
                 'there is no line. There is a sequence, it has an order, and it takes '
                 'much longer than anyone expects.'},

 'blocks': [
  {'type': 'text', 'h': 'The heart stops. Almost nothing else does.',
   'p': ['Your brain has about ten seconds of oxygen left in it. That part is quick.',
         'Everything else keeps going. Your cells do not know anything has happened. '
         'They have fuel, they have a job, and they carry on doing it for '
         '<strong>minutes to hours</strong>.']},

  {'type': 'scene', 'tone': 'ember', 'scene': 'pulse',
   'h': 'The rhythm slows, and then it does not come back',
   'p': 'Everything downstream of it keeps running on what it already has.'},

  {'type': 'text', 'h': 'This is why transplants are possible at all',
   'p': ['A donated heart can be restarted in someone else hours after its owner died. '
         'A cornea works after a day. Bone and skin last longer still.',
         'None of that would work if death were a single instant.']},

  {'type': 'turn', 'tone': 'solar',
   'text': 'You do not die all at once. Different parts of you stop at different times, over hours.'},

  {'type': 'figure', 'tone': 'void',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What is still viable at different times after the heart stops</title>
  <g id="organs"></g>
  <line class="f-faint" x1="30" y1="252" x2="630" y2="252"/>
  <circle id="mark" cx="30" cy="252" r="6" fill="#FCD34D"/>
  <text class="f-label" x="30" y="276">HEART STOPS</text>
  <text class="f-label" x="630" y="276" text-anchor="end">24 HOURS</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="mins">Time since the heart stopped</label>
  <input type="range" id="mins" min="0" max="1440" step="1" value="0">
  <span class="readout" id="minsOut">0 min</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var mins = document.getElementById('mins');
// roughly how long each tissue stays viable without circulation
var ORGANS = [
  { n: 'Brain',   life: 0.3,  col: '#F472B6' },
  { n: 'Heart',   life: 240,  col: '#FB7185' },
  { n: 'Liver',   life: 720,  col: '#FBBF24' },
  { n: 'Kidneys', life: 1080, col: '#A3E635' },
  { n: 'Cornea',  life: 1440, col: '#22D3EE' },
  { n: 'Skin',    life: 1440, col: '#A78BFA' }
];
var host = document.getElementById('organs'), rows = [];
ORGANS.forEach(function (o, i) {
  var g = document.createElementNS(NS, 'g');
  var y = 40 + i * 33;
  g.innerHTML =
    '<text x="30" y="' + (y + 5) + '" class="f-label">' + o.n.toUpperCase() + '</text>' +
    '<rect x="150" y="' + (y - 9) + '" width="380" height="16" rx="8" fill="rgba(255,255,255,.12)"/>' +
    '<rect x="150" y="' + (y - 9) + '" width="380" height="16" rx="8" fill="' + o.col + '"/>' +
    '<text x="548" y="' + (y + 5) + '" class="f-label">alive</text>';
  host.appendChild(g);
  rows.push({ o: o, bar: g.children[2], lab: g.children[3] });
});

function draw() {
  var m = +mins.value;
  document.getElementById('minsOut').textContent =
    m < 60 ? m + ' min' : (m / 60).toFixed(1) + ' hours';
  document.getElementById('mark').setAttribute('cx', 30 + (m / 1440) * 600);
  rows.forEach(function (r) {
    var left = Math.max(0, 1 - m / r.o.life);
    r.bar.setAttribute('width', 380 * left);
    r.lab.textContent = left > 0 ? 'alive' : 'gone';
    r.lab.setAttribute('opacity', left > 0 ? 1 : .45);
  });
}
mins.addEventListener('input', draw);
draw();
''',
   'caption': 'The brain goes first and goes fast. Everything else has hours, which is '
              'exactly the window transplant teams are working inside.'},

  {'type': 'scene', 'tone': 'forest', 'scene': 'swarm',
   'h': 'Then the ones that helped you take over',
   'p': 'The microbes that spent your life digesting your food begin, without any '
        'change of behaviour, to digest you. They were never doing anything else.'},

  {'type': 'text', 'h': 'Which is why the definition had to change',
   'p': ['For most of history, death meant the heart stopped. Then we learned to '
         'restart hearts, and the definition stopped working.',
         'Now the line is drawn at the brain, because that is the one part that cannot '
         'be replaced, restarted, or waited on.']},
 ],

 'zoomout': {'tone': 'void',
   'text': 'Nothing about you is destroyed. Every atom carries on, gets taken up, and '
           'ends up somewhere else. The arrangement is what ends — and the arrangement '
           'was always the temporary part.'},
},

# ================================================================== 12
{
 'slug': 'why-do-we-sleep',
 'kicker': 'Your body',
 'card_tone': 'dusk', 'card_scene': 'sleepcycle',
 'featured': True,
 'title': 'Why do we sleep?',
 'teaser': 'A third of your life, unconscious and defenceless. Evolution kept it anyway, so it must be worth it.',
 'hero': {'tone': 'dusk', 'scene': 'sleepcycle',
   'standfirst': 'Lying still and unaware for eight hours is about the most dangerous '
                 'thing an animal can do. Every animal does it anyway. Whatever sleep '
                 'is for, it is worth being eaten over.'},

 'blocks': [
  {'type': 'text', 'h': 'It is far too expensive to be an accident',
   'p': ['You cannot eat, defend yourself, or watch for anything while asleep. If it '
         'were optional, something would have dropped it by now.',
         'Nothing has. Not one animal with a brain has managed to do without it.']},

  {'type': 'scene', 'tone': 'nebula', 'scene': 'sleepcycle',
   'h': 'A night is four or five loops, not one long blank',
   'p': 'You sink into deep sleep, climb back toward dreaming, and repeat. The deep '
        'part loads the front of the night; the dreaming part loads the end.'},

  {'type': 'text', 'h': 'The brain cleans itself while you are out',
   'p': ['During deep sleep the gaps between brain cells widen, and fluid is pushed '
         'through to flush out the waste of the day.',
         'It appears to be far more effective asleep than awake — which is a good '
         'reason the brain would rather do it while you are not using it.']},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'Sleep is not the brain switching off. It is the brain doing the maintenance it cannot do while you are using it.'},

  {'type': 'figure', 'tone': 'dusk',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What changes with different amounts of sleep</title>
  <g id="bars"></g>
  <text class="f-label" x="30" y="284" id="verdict">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="hrs">Hours of sleep</label>
  <input type="range" id="hrs" min="0" max="10" step="1" value="8">
  <span class="readout" id="hrsOut">8 hours</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var hrs = document.getElementById('hrs');
var MEASURES = [
  { n: 'Reaction time', col: '#22D3EE', best: 8 },
  { n: 'Memory',        col: '#A3E635', best: 8 },
  { n: 'Mood',          col: '#FBBF24', best: 8 },
  { n: 'Immune system', col: '#F472B6', best: 8 }
];
var host = document.getElementById('bars'), rows = [];
MEASURES.forEach(function (m, i) {
  var g = document.createElementNS(NS, 'g'), y = 48 + i * 52;
  g.innerHTML =
    '<text x="30" y="' + (y - 12) + '" class="f-label">' + m.n.toUpperCase() + '</text>' +
    '<rect x="30" y="' + (y - 2) + '" width="600" height="18" rx="9" fill="rgba(255,255,255,.12)"/>' +
    '<rect x="30" y="' + (y - 2) + '" width="0" height="18" rx="9" fill="' + m.col + '"/>';
  host.appendChild(g);
  rows.push({ m: m, bar: g.children[2] });
});

function draw() {
  var h = +hrs.value;
  document.getElementById('hrsOut').textContent = h + (h === 1 ? ' hour' : ' hours');
  rows.forEach(function (r) {
    // performance climbs steeply to about eight hours and then flattens
    var v = Math.min(1, Math.pow(h / r.m.best, 1.7));
    r.bar.setAttribute('width', 600 * v);
  });
  document.getElementById('verdict').textContent =
    h <= 2 ? 'AFTER A FULL NIGHT AWAKE YOU PERFORM LIKE SOMEONE OVER THE DRINK-DRIVE LIMIT' :
    h <= 5 ? 'YOU WILL FEEL FINE. YOU WILL NOT BE FINE.' :
    h <= 7 ? 'CLOSE, BUT THE DEBT STILL ADDS UP NIGHT AFTER NIGHT' :
             'THIS IS WHAT MOST ADULTS ACTUALLY NEED';
}
hrs.addEventListener('input', draw);
draw();
''',
   'caption': 'The cruel part is that the feeling of being fine recovers long before '
              'the performance does. People running on five hours consistently rate '
              'themselves as unaffected.'},

  {'type': 'scene', 'tone': 'rose', 'scene': 'attention',
   'h': 'Dreams look like the filing being done',
   'p': 'The night replays pieces of the day, keeps some, drops most, and files what '
        'is left next to things you already knew.'},

  {'type': 'text', 'h': 'What happens if you stop',
   'p': ['A day without sleep is roughly being drunk. Two days and your body starts '
         'forcing microsleeps — seconds at a time, whether you agree or not.',
         'Push much further and thinking falls apart entirely. There is no known way '
         'to train yourself out of needing it.']},
 ],

 'zoomout': {'tone': 'dusk',
   'text': 'You will spend around twenty-six years of your life asleep. Not lost time — '
           'it is the maintenance window that makes the other fifty-odd years work at '
           'all.'},
},

# ================================================================== 13
{
 'slug': 'how-many-people-ever-lived',
 'kicker': 'People',
 'card_tone': 'deepsea', 'card_scene': 'crowd',
 'featured': True,
 'title': 'How many people have ever lived?',
 'teaser': 'Around 117 billion. The dead outnumber the living by roughly fourteen to one.',
 'hero': {'tone': 'deepsea', 'scene': 'crowd',
   'standfirst': 'Everyone who has ever been born, added up, comes to about 117 billion '
                 'people. Eight billion of them are here now. The rest is the crowd '
                 'standing behind you.'},

 'blocks': [
  {'type': 'text', 'h': 'You can actually estimate this',
   'p': ['Take a start date, take the best guess at population at each point in '
         'history, apply a birth rate, and add it up.',
         'The answer lands near <strong>117 billion</strong>. It is an estimate with '
         'real error bars, but the scale is solid.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'crowd',
   'h': 'For every person alive, about fourteen have already gone',
   'p': 'The bright ones are everyone here now. The rest is everyone else who ever was.'},

  {'type': 'text', 'h': 'Most of that crowd never got to grow up',
   'p': ['For nearly all of history, something close to <strong>half of all children '
         'died before the age of fifteen</strong>.',
         'That is the single biggest thing separating your life from almost every '
         'human life that came before it, and it changed within about four '
         'generations.']},

  {'type': 'turn', 'tone': 'solar',
   'text': 'You are living in the most crowded moment in human history, and also the safest one anybody has ever been born into.'},

  {'type': 'figure', 'tone': 'deepsea',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Population alive against the total who had ever lived</title>
  <line class="f-faint" x1="50" y1="240" x2="630" y2="240"/>
  <path id="everLine" d="" fill="none" stroke="#A78BFA" stroke-width="3"/>
  <path id="aliveLine" d="" fill="none" stroke="#22D3EE" stroke-width="3"/>
  <line id="cursor" class="f-faint" x1="50" y1="40" x2="50" y2="240"/>
  <text class="f-label" x="50" y="264">10,000 BC</text>
  <text class="f-label" x="630" y="264" text-anchor="end">TODAY</text>
  <text class="f-label" x="50" y="40">ALIVE NOW</text>
  <text class="f-value" id="aliveTxt" x="50" y="72" style="font-size:24px;fill:#22D3EE">&#8212;</text>
  <text class="f-label" x="360" y="40">EVER BORN, BY THEN</text>
  <text class="f-value" id="everTxt" x="360" y="72" style="font-size:24px;fill:#A78BFA">&#8212;</text>
  <text class="f-label" id="ratioTxt" x="50" y="290">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="yr">Year</label>
  <input type="range" id="yr" min="-10000" max="2026" step="50" value="2026">
  <span class="readout" id="yrOut">2026</span>
</div>''',
   'js': '''
var yr = document.getElementById('yr');

// crude but honestly shaped: population creeps for millennia, then explodes
function alive(y) {
  if (y < -8000) return 0.005;
  var f = (y + 10000) / 12026;
  return 0.005 + 8.0 * Math.pow(f, 14);
}
function ever(y) {
  var f = (y + 10000) / 12026;
  return 117 * Math.pow(f, 2.4);
}

function path(fn, top) {
  var d = '';
  for (var i = 0; i <= 120; i++) {
    var y = -10000 + (12026 * i / 120);
    var x = 50 + (i / 120) * 580;
    var py = 240 - (fn(y) / top) * 190;
    d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + py.toFixed(1);
  }
  return d;
}
document.getElementById('everLine').setAttribute('d', path(ever, 117));
document.getElementById('aliveLine').setAttribute('d', path(alive, 117));

function draw() {
  var y = +yr.value;
  document.getElementById('yrOut').textContent = y < 0 ? Math.abs(y) + ' BC' : y;
  var a = alive(y), e = ever(y);
  document.getElementById('aliveTxt').textContent = a.toFixed(2) + ' billion';
  document.getElementById('everTxt').textContent = e.toFixed(0) + ' billion';
  document.getElementById('ratioTxt').textContent =
    'THAT IS ABOUT ' + Math.round(e / Math.max(a, .001)) + ' PEOPLE WHO HAVE LIVED FOR EVERY ONE ALIVE';
  var x = 50 + ((y + 10000) / 12026) * 580;
  document.getElementById('cursor').setAttribute('x1', x);
  document.getElementById('cursor').setAttribute('x2', x);
}
yr.addEventListener('input', draw);
draw();
''',
   'caption': 'The cyan line is everyone alive at that moment. The violet one is '
              'everyone who had ever lived by then. Notice how recently the cyan line '
              'does anything at all.'},

  {'type': 'scene', 'tone': 'rose', 'scene': 'crowd',
   'h': 'Almost everyone who ever lived, lived without any of this',
   'p': 'No anaesthetic, no clean water, no idea what a germ was. That was the normal '
        'human experience until about six generations ago.'},

  {'type': 'text', 'h': 'And the ratio is going to keep shifting',
   'p': ['Population growth is slowing worldwide. Birth rates have fallen faster than '
         'almost anyone predicted.',
         'The share of all humans who are alive right now is about as high as it is '
         'ever likely to get.']},
 ],

 'zoomout': {'tone': 'deepsea',
   'text': 'You are one of 117 billion, and one of the very small number who got '
           'antibiotics, and a reasonable chance of reaching seventy. On the balance '
           'of everyone who ever tried this, that is an extraordinary draw.'},
},

# ================================================================== 14
{
 'slug': 'why-do-we-get-bored',
 'kicker': 'Mind',
 'card_tone': 'nebula', 'card_scene': 'attention',
 'featured': False,
 'title': 'Why do we get bored?',
 'teaser': 'Boredom feels like nothing happening. It is one of the most useful signals your brain sends.',
 'hero': {'tone': 'nebula', 'scene': 'attention',
   'standfirst': 'Boredom is genuinely unpleasant — people will give themselves small '
                 'electric shocks rather than sit alone with nothing to do. That is a '
                 'strange amount of pressure for a feeling that seems to do nothing.'},

 'blocks': [
  {'type': 'text', 'h': 'It is an alarm, not a mood',
   'p': ['Bored means two things at once: you want to be engaged with something, and '
         'nothing available is doing it.',
         'That gap is the whole feeling. It is your attention system reporting that '
         '<strong>it is being wasted</strong>.']},

  {'type': 'scene', 'tone': 'dusk', 'scene': 'attention',
   'h': 'Attention will not sit still for something worthless',
   'p': 'The focus keeps sliding off, and everything at the edges starts looking more '
        'interesting than the middle.'},

  {'type': 'text', 'h': 'And that is exactly the point',
   'p': ['An animal that felt fine doing nothing forever would sit in one place and '
         'starve. Boredom is the push that makes you go and look.',
         'People made to do something tedious then score higher on tests of coming up '
         'with new ideas. The restlessness is doing something.']},

  {'type': 'turn', 'tone': 'solar',
   'text': 'Boredom is not the absence of something to do. It is your brain telling you that what you are doing is not worth it.'},

  {'type': 'figure', 'tone': 'nebula',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How engaged you are at different levels of challenge</title>
  <path id="curve" d="" fill="none" stroke="#A3E635" stroke-width="3.5"/>
  <line class="f-faint" x1="50" y1="230" x2="630" y2="230"/>
  <circle id="you" cx="340" cy="80" r="10" fill="#FBBF24"/>
  <text class="f-label" x="50" y="256">TOO EASY</text>
  <text class="f-label" x="340" y="256" text-anchor="middle">JUST HARD ENOUGH</text>
  <text class="f-label" x="630" y="256" text-anchor="end">TOO HARD</text>
  <text class="f-label" x="50" y="40">YOU FEEL</text>
  <text class="f-value" id="feelTxt" x="50" y="74" style="font-size:26px">&#8212;</text>
  <text class="f-label" id="tipTxt" x="50" y="290">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="chal">How hard the task is</label>
  <input type="range" id="chal" min="0" max="100" step="1" value="50">
  <span class="readout" id="chalOut">&#8212;</span>
</div>''',
   'js': '''
var chal = document.getElementById('chal');

function engage(x) {           // an upside-down U: bored, then absorbed, then swamped
  return Math.exp(-Math.pow((x - 50) / 26, 2));
}

var d = '';
for (var i = 0; i <= 100; i++) {
  d += (i ? 'L' : 'M') + (50 + i * 5.8).toFixed(1) + ' ' + (230 - engage(i) * 170).toFixed(1);
}
document.getElementById('curve').setAttribute('d', d);

function draw() {
  var x = +chal.value, e = engage(x);
  document.getElementById('you').setAttribute('cx', 50 + x * 5.8);
  document.getElementById('you').setAttribute('cy', 230 - e * 170);
  document.getElementById('chalOut').textContent =
    x < 30 ? 'far too easy' : x < 45 ? 'a bit easy' : x < 58 ? 'about right' : x < 75 ? 'a bit hard' : 'far too hard';
  document.getElementById('feelTxt').textContent =
    x < 30 ? 'bored' : x < 45 ? 'restless' : x < 58 ? 'absorbed' : x < 75 ? 'stretched' : 'overwhelmed';
  document.getElementById('tipTxt').textContent =
    x < 45 ? 'MAKE IT HARDER, NOT LONGER' :
    x > 62 ? 'BREAK IT INTO A SMALLER PIECE' :
             'THIS IS THE BAND WHERE TIME DISAPPEARS';
}
chal.addEventListener('input', draw);
draw();
''',
   'caption': 'Boredom and panic are the same curve at opposite ends. The fix for '
              'boredom is almost never more entertainment — it is a harder version of '
              'what you are already doing.'},

  {'type': 'scene', 'tone': 'ember', 'scene': 'flicker',
   'h': 'Why a phone makes it worse',
   'p': 'An endless feed is engaging enough to stop the discomfort and never engaging '
        'enough to satisfy it. The alarm gets muffled instead of answered.'},

  {'type': 'text', 'h': 'Being bored on purpose',
   'p': ['Ideas turn up in showers and on walks because those are the last places left '
         'with nothing to look at.',
         'If you never let yourself be bored, you never get the part that comes after '
         'it.']},
 ],

 'zoomout': {'tone': 'nebula',
   'text': 'Boredom is a demand for something better, and it is one of the few '
           'feelings that goes away only when you actually do something worth doing.'},
},

# ================================================================== 15
{
 'slug': 'bottom-of-the-ocean',
 'kicker': 'Earth',
 'card_tone': 'deepsea', 'card_scene': 'depths',
 'featured': False,
 'title': 'What lives at the bottom of the ocean?',
 'teaser': 'Eleven kilometres down, in permanent dark under crushing pressure, things are still alive.',
 'hero': {'tone': 'deepsea', 'scene': 'depths',
   'standfirst': 'Sunlight gives up after about two hundred metres. The sea keeps going '
                 'for another eleven thousand — and every layer below that light has '
                 'something living in it.'},

 'blocks': [
  {'type': 'text', 'h': 'Almost all of the ocean is dark',
   'p': ['The bright blue part you can picture is a thin skin on the top. Below two '
         'hundred metres, there is not enough light for a plant to live.',
         'That dark part is <strong>most of the living space on this planet</strong>, '
         'by a very long way.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'depths',
   'h': 'So they brought their own light',
   'p': 'Below about a kilometre, most of what you would see makes its own — for '
        'hunting, for hiding, and for finding each other in the dark.'},

  {'type': 'steps', 'tone': 'nebula', 'h': 'Going down',
   'items': [
     {'h': '0 to 200 m', 'p': 'Sunlight. Nearly everything you can name lives up here, in about two per cent of the volume.'},
     {'h': '200 to 1,000 m', 'p': 'Twilight. Animals commute up at night to feed and sink back down by day — the largest migration on Earth, happening daily.'},
     {'h': '1,000 to 6,000 m', 'p': 'Total dark, near freezing. Food arrives as a slow drizzle of dead things from above.'},
     {'h': '6,000 to 11,000 m', 'p': 'The trenches. Pressure over a thousand times what you feel now. Still inhabited.'}]},

  {'type': 'turn', 'tone': 'ember',
   'text': 'More people have stood on the Moon than have been to the deepest point in the sea.'},

  {'type': 'figure', 'tone': 'deepsea',
   'svg': '''<svg viewBox="0 0 660 320" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Conditions and life at increasing ocean depth</title>
  <rect id="water" x="30" y="30" width="260" height="250" rx="10" fill="rgba(34,211,238,.16)"/>
  <circle id="sub" cx="160" cy="60" r="11" fill="#FCD34D"/>
  <text class="f-label" x="330" y="60">PRESSURE</text>
  <text class="f-value" id="presTxt" x="330" y="94" style="font-size:24px">&#8212;</text>
  <text class="f-label" x="330" y="140">LIGHT</text>
  <text class="f-value" id="lightTxt" x="330" y="174" style="font-size:22px">&#8212;</text>
  <text class="f-label" x="330" y="220">WHAT IS DOWN HERE</text>
  <text class="f-value" id="lifeTxt" x="330" y="254" style="font-size:20px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="30" y="306">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="dep">Depth</label>
  <input type="range" id="dep" min="0" max="11000" step="10" value="0">
  <span class="readout" id="depOut">0 m</span>
</div>''',
   'js': '''
var dep = document.getElementById('dep');

function draw() {
  var d = +dep.value;
  document.getElementById('depOut').textContent =
    d < 1000 ? d + ' m' : (d / 1000).toFixed(1) + ' km';
  document.getElementById('sub').setAttribute('cy', 60 + (d / 11000) * 205);
  // one extra atmosphere for every ten metres
  document.getElementById('presTxt').textContent = (1 + d / 10).toFixed(0) + ' atmospheres';
  document.getElementById('lightTxt').textContent =
    d < 40 ? 'bright' : d < 200 ? 'dim blue' : d < 1000 ? 'the last traces' : 'none at all';
  document.getElementById('lifeTxt').textContent =
    d < 200 ? 'almost everything you can name' :
    d < 1000 ? 'squid, lanternfish, jellyfish' :
    d < 4000 ? 'anglerfish and other light-makers' :
    d < 6000 ? 'sea cucumbers, brittle stars, worms' :
               'snailfish, amphipods, bacteria';
  document.getElementById('water').setAttribute('fill',
    d < 200 ? 'rgba(34,211,238,.16)' : d < 1000 ? 'rgba(96,165,250,.13)' : 'rgba(167,139,250,.1)');
  document.getElementById('noteTxt').textContent =
    d > 10000 ? 'AT THIS DEPTH A STYROFOAM CUP SHRINKS TO THE SIZE OF A THIMBLE' :
    d > 6000  ? 'THE TRENCHES. FEWER VISITS THAN THE MOON HAS HAD.' :
    d > 1000  ? 'FOOD FALLS FROM ABOVE AS A CONSTANT SLOW DRIZZLE' : '';
}
dep.addEventListener('input', draw);
draw();
''',
   'caption': 'Drag all the way down. Pressure climbs by one atmosphere every ten '
              'metres, so at the bottom of the deepest trench you are under about a '
              'thousand — and something still lives there.'},

  {'type': 'scene', 'tone': 'ember', 'scene': 'virus',
   'h': 'And some of it never needed the Sun at all',
   'p': 'Around hot vents on the sea floor, whole communities run on chemicals from '
        'inside the Earth. No sunlight anywhere in the chain.'},

  {'type': 'text', 'h': 'Why that matters beyond Earth',
   'p': ['Before we found those vents, "life needs sunlight" was a safe assumption. It '
         'turned out to be a local habit rather than a rule.',
         'It is a large part of why the icy moons of Jupiter and Saturn, with dark '
         'oceans under their shells, are now serious places to go looking.']},
 ],

 'zoomout': {'tone': 'deepsea',
   'text': 'We have better maps of Mars than of our own sea floor. The largest habitat '
           'on this planet is the one we have looked at least.'},
},

# ================================================================== 16
{
 'slug': 'why-do-we-age',
 'kicker': 'Your body',
 'card_tone': 'rose', 'card_scene': 'telomere',
 'featured': False,
 'title': 'Why do we get old?',
 'teaser': 'Ageing is not simple wear and tear. Some animals barely do it at all.',
 'hero': {'tone': 'rose', 'scene': 'telomere',
   'standfirst': 'A car wears out because nothing repairs it. You are repaired '
                 'constantly, by trillions of cells whose entire job is maintenance. '
                 'So why does it stop working?'},

 'blocks': [
  {'type': 'text', 'h': 'You are rebuilt all the time',
   'p': ['Your gut lining is days old. Your skin is weeks old. Even bone replaces '
         'itself over about a decade.',
         'If ageing were just things wearing out, constant rebuilding should hold it '
         'off indefinitely. It does not.']},

  {'type': 'scene', 'tone': 'nebula', 'scene': 'telomere',
   'h': 'Every copy is slightly worse than the last',
   'p': 'Cells carry protective caps on their DNA that get shorter each time they '
        'divide. When the cap runs out, the cell stops dividing for good.'},

  {'type': 'text', 'h': 'And the repair crew ages too',
   'p': ['Worn-out cells do not always leave quietly. Many stick around, stop working '
         'and start leaking signals that inflame the tissue near them.',
         'So damage accumulates while the ability to fix it declines. Those two curves '
         'crossing is a decent working definition of <strong>getting old</strong>.']},

  {'type': 'turn', 'tone': 'solar',
   'text': 'Evolution has no reason to keep you in good repair after you have had children. Ageing is the point where it stops paying.'},

  {'type': 'figure', 'tone': 'rose',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Damage building up against the body's ability to repair it</title>
  <line class="f-faint" x1="50" y1="230" x2="630" y2="230"/>
  <path id="dmg" d="" fill="none" stroke="#FB7185" stroke-width="3.5"/>
  <path id="rep" d="" fill="none" stroke="#34D399" stroke-width="3.5"/>
  <line id="cursor" class="f-faint" x1="50" y1="40" x2="50" y2="230"/>
  <text class="f-label" x="50" y="254">BIRTH</text>
  <text class="f-label" x="630" y="254" text-anchor="end">100</text>
  <text class="f-label" x="50" y="36">DAMAGE (PINK) &#183; REPAIR (GREEN)</text>
  <text class="f-value" id="stateTxt" x="50" y="286" style="font-size:20px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="age">Age</label>
  <input type="range" id="age" min="0" max="100" step="1" value="30">
  <span class="readout" id="ageOut">30</span>
</div>''',
   'js': '''
var age = document.getElementById('age');

function damage(a) { return Math.min(1, Math.pow(a / 100, 1.9) * 1.35); }
function repair(a) { return Math.max(.05, 1 - Math.pow(a / 100, 1.6) * 1.15); }

function path(fn) {
  var d = '';
  for (var i = 0; i <= 100; i++) {
    d += (i ? 'L' : 'M') + (50 + i * 5.8).toFixed(1) + ' ' + (230 - fn(i) * 180).toFixed(1);
  }
  return d;
}
document.getElementById('dmg').setAttribute('d', path(damage));
document.getElementById('rep').setAttribute('d', path(repair));

function draw() {
  var a = +age.value;
  document.getElementById('ageOut').textContent = a;
  var x = 50 + a * 5.8;
  document.getElementById('cursor').setAttribute('x1', x);
  document.getElementById('cursor').setAttribute('x2', x);
  var d = damage(a), r = repair(a);
  document.getElementById('stateTxt').textContent =
    r > d + .35 ? 'Repair is winning comfortably' :
    r > d       ? 'Still ahead, but the gap is closing' :
    r > d - .3  ? 'The lines have crossed. This is what ageing feels like.' :
                  'Damage is accumulating faster than anything can fix it';
}
age.addEventListener('input', draw);
draw();
''',
   'caption': 'Nothing dramatic happens at any particular age. The two lines simply '
              'cross, somewhere in your forties or fifties, and after that the balance '
              'runs the other way.'},

  {'type': 'scene', 'tone': 'forest', 'scene': 'cells',
   'h': 'Some animals barely bother with it',
   'p': 'A bowhead whale can pass two hundred. Some tortoises show almost no rise in '
        'death rate with age at all. Ageing is clearly not compulsory.'},

  {'type': 'text', 'h': 'Which is why anyone thinks it is treatable',
   'p': ['If ageing were simple decay, there would be nothing to do about it. Because '
         'it is a set of specific processes, each one is a thing you could target.',
         'Clearing out worn-out cells extends healthy life in mice. Whether any of it '
         'transfers to people is genuinely not known yet.']},
 ],

 'zoomout': {'tone': 'rose',
   'text': 'Ageing looks less like a law of nature and more like a maintenance contract '
           'that runs out. That does not make it easy to renegotiate — but it does make '
           'it the kind of problem that can, in principle, be worked on.'},
},

# ================================================================== 17
{
 'slug': 'is-a-virus-alive',
 'kicker': 'Life',
 'card_tone': 'ember', 'card_scene': 'virus',
 'featured': False,
 'title': 'Is a virus alive?',
 'teaser': 'It cannot eat, move, grow or reproduce by itself. It is also extraordinarily good at what it does.',
 'hero': {'tone': 'ember', 'scene': 'virus',
   'standfirst': 'A virus sits at the exact edge of the definition of life, and biology '
                 'has never fully agreed which side it falls on. That is not a gap in '
                 'our knowledge — it is a problem with the definition.'},

 'blocks': [
  {'type': 'text', 'h': 'A virus is instructions in a box',
   'p': ['Strip one down and you find a short set of genetic instructions wrapped in a '
         'protein shell. Sometimes a fatty coat over that.',
         'That is the entire organism. No mouth, no engine, no way of making anything. '
         '<strong>Left alone, it does nothing at all — indefinitely.</strong>']},

  {'type': 'scene', 'tone': 'nebula', 'scene': 'virus',
   'h': 'It only becomes anything when it finds a cell',
   'p': 'The shell docks, the instructions go in, and the cell starts building copies '
        'of the thing that infected it.'},

  {'type': 'steps', 'tone': 'forest', 'h': 'The usual tests for being alive',
   'items': [
     {'h': 'Uses energy', 'p': 'A virus does not. It has no metabolism of any kind. FAILS.'},
     {'h': 'Grows', 'p': 'It never grows. It is assembled at full size. FAILS.'},
     {'h': 'Reproduces', 'p': 'Only by making a cell do it. On its own, never. HALF.'},
     {'h': 'Evolves', 'p': 'Spectacularly well. This is why flu jabs are yearly. PASSES.'}]},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'A virus is not alive, and not dead. It is a set of instructions waiting for a machine that can read them.'},

  {'type': 'figure', 'tone': 'ember',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Which tests for life a virus passes</title>
  <g id="tests"></g>
  <text class="f-label" x="30" y="252">ON THIS DEFINITION, A VIRUS IS</text>
  <text class="f-value" id="verdict" x="30" y="286" style="font-size:26px">&#8212;</text>
</svg>''',
   'controls': '''<div class="chips" role="group" aria-label="What you require of life">
  <button class="chip" id="tEnergy" aria-pressed="true">Uses energy</button>
  <button class="chip" id="tGrow" aria-pressed="true">Grows</button>
  <button class="chip" id="tRepro" aria-pressed="true">Reproduces alone</button>
  <button class="chip" id="tEvolve" aria-pressed="true">Evolves</button>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
// whether a virus meets each requirement
var TESTS = [
  { id: 'tEnergy', n: 'Uses energy',       pass: false, col: '#FB7185' },
  { id: 'tGrow',   n: 'Grows',             pass: false, col: '#FBBF24' },
  { id: 'tRepro',  n: 'Reproduces alone',  pass: false, col: '#F472B6' },
  { id: 'tEvolve', n: 'Evolves',           pass: true,  col: '#A3E635' }
];
var host = document.getElementById('tests'), rows = [];
TESTS.forEach(function (t, i) {
  var g = document.createElementNS(NS, 'g'), y = 54 + i * 44;
  g.innerHTML =
    '<circle cx="46" cy="' + y + '" r="13" fill="' + t.col + '"/>' +
    '<text x="46" y="' + (y + 6) + '" text-anchor="middle" class="f-value" style="font-size:15px;fill:#0b1220">' +
      (t.pass ? 'Y' : 'N') + '</text>' +
    '<text x="80" y="' + (y + 6) + '" class="f-value" style="font-size:18px">' + t.n + '</text>' +
    '<text x="380" y="' + (y + 6) + '" class="f-label">' + (t.pass ? 'a virus does this' : 'a virus cannot') + '</text>';
  host.appendChild(g);
  rows.push({ t: t, g: g });
});

function draw() {
  var required = TESTS.filter(function (t) {
    return document.getElementById(t.id).getAttribute('aria-pressed') === 'true';
  });
  rows.forEach(function (r) {
    var on = document.getElementById(r.t.id).getAttribute('aria-pressed') === 'true';
    r.g.setAttribute('opacity', on ? 1 : .25);
  });
  var fails = required.filter(function (t) { return !t.pass; }).length;
  document.getElementById('verdict').textContent =
    required.length === 0 ? 'alive, but so is a rock' :
    fails === 0 ? 'alive' :
    fails === required.length ? 'not alive' : 'somewhere in between';
}
TESTS.forEach(function (t) {
  var b = document.getElementById(t.id);
  b.addEventListener('click', function () {
    b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    draw();
  });
});
draw();
''',
   'caption': 'Switch requirements off and on. The answer changes — which tells you the '
              'argument was never about viruses. It was about where we drew the line.'},

  {'type': 'scene', 'tone': 'void', 'scene': 'swarm',
   'h': 'There are more of them than anything else',
   'p': 'Around ten to the thirty-first, by rough count. Laid end to end they would '
        'reach further than the nearest galaxies. Most infect bacteria, not you.'},

  {'type': 'text', 'h': 'And some of them are in you permanently',
   'p': ['About eight per cent of your DNA came from viruses that infected your '
         'ancestors and never left.',
         'One of those leftover genes is essential for building a placenta. Mammals '
         'may owe live birth to an ancient infection.']},
 ],

 'zoomout': {'tone': 'ember',
   'text': 'Nature does not care about our categories. We drew a line called "alive", '
           'and viruses sat down exactly on top of it and have not moved since.'},
},

# ================================================================== 18
{
 'slug': 'if-everyone-vanished',
 'kicker': 'Earth',
 'card_tone': 'forest', 'card_scene': 'overgrow',
 'featured': False,
 'title': 'What if every human vanished tomorrow?',
 'teaser': 'The lights go out in hours. The cities last centuries. A few things we made outlast all of it.',
 'hero': {'tone': 'forest', 'scene': 'overgrow',
   'standfirst': 'Not an apocalypse — just everybody gone, everything else left exactly '
                 'as it is. What happens next is a good way of finding out how much of '
                 'the world is being actively held in place.'},

 'blocks': [
  {'type': 'text', 'h': 'Hours: the lights go out',
   'p': ['Most power stations need someone to feed them. Within hours the grid fails, '
         'and almost everywhere goes dark that first night.',
         'For the first time in two centuries, you could see the stars from the middle '
         'of a city.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'stars',
   'h': 'The night sky comes back immediately',
   'p': 'No lights, no aircraft, no noise. Within a day the planet sounds and looks the '
        'way it did for the previous few hundred thousand years.'},

  {'type': 'steps', 'tone': 'deepsea', 'h': 'Then it is just a matter of waiting',
   'items': [
     {'h': 'Days', 'p': 'Pumps stop. Underground railways flood. Livestock and pets are on their own.'},
     {'h': 'Years', 'p': 'Water gets into every roof. Frost cracks it wider. Plants take the roads apart from underneath.'},
     {'h': 'Decades', 'p': 'Wooden buildings collapse. Fires run unchecked through cities. Rivers go back to their old courses.'},
     {'h': 'Centuries', 'p': 'Steel corrodes through and the tall buildings come down. Forest covers most of what was city.'}]},

  {'type': 'turn', 'tone': 'solar',
   'text': 'Nature does not have to fight the city. It only has to wait, and it is extremely good at waiting.'},

  {'type': 'figure', 'tone': 'forest',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What is left of human things as time passes</title>
  <g id="things"></g>
  <text class="f-label" id="eraTxt" x="30" y="286">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="t">Time since we vanished</label>
  <input type="range" id="t" min="0" max="100" step="1" value="0">
  <span class="readout" id="tOut">day one</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var tt = document.getElementById('t');
// how long each thing survives, in log10(years)
var THINGS = [
  { n: 'The power grid',   life: -2.5, col: '#FBBF24' },
  { n: 'Glass windows',    life: 1.4,  col: '#22D3EE' },
  { n: 'Wooden houses',    life: 2,    col: '#A3E635' },
  { n: 'Steel towers',     life: 2.6,  col: '#60A5FA' },
  { n: 'Concrete dams',    life: 3.2,  col: '#A78BFA' },
  { n: 'Plastic',          life: 3.6,  col: '#F472B6' },
  { n: 'Footprints on the Moon', life: 7, col: '#FCD34D' }
];
var host = document.getElementById('things'), rows = [];
THINGS.forEach(function (o, i) {
  var g = document.createElementNS(NS, 'g'), y = 40 + i * 32;
  g.innerHTML =
    '<circle cx="42" cy="' + y + '" r="8" fill="' + o.col + '"/>' +
    '<text x="66" y="' + (y + 5) + '" class="f-value" style="font-size:16px">' + o.n + '</text>' +
    '<text x="470" y="' + (y + 5) + '" class="f-label">still here</text>';
  host.appendChild(g);
  rows.push({ o: o, dot: g.children[0], lab: g.children[2] });
});

function draw() {
  var p = +tt.value / 10 - 3;             // log10 years, from about a day to 10^7
  var yrs = Math.pow(10, p);
  document.getElementById('tOut').textContent =
    yrs < 0.01 ? 'day one' :
    yrs < 1 ? Math.round(yrs * 365) + ' days' :
    yrs < 1000 ? Math.round(yrs) + ' years' :
    Math.round(yrs).toExponential(0).replace('e+', ' x 10^') + ' years';
  rows.forEach(function (r) {
    var gone = p > r.o.life;
    r.dot.setAttribute('opacity', gone ? .2 : 1);
    r.lab.textContent = gone ? 'gone' : 'still here';
    r.lab.setAttribute('opacity', gone ? .4 : 1);
  });
  document.getElementById('eraTxt').textContent =
    p < -1 ? 'THE GRID IS THE FIRST THING TO GO, AND IT GOES ALMOST IMMEDIATELY' :
    p < 2  ? 'WATER AND FROST ARE DOING MOST OF THE WORK NOW' :
    p < 3.4 ? 'THE CITIES ARE FOREST. ONLY THE HEAVIEST THINGS REMAIN.' :
              'NOTHING BUILT ON EARTH IS LEFT. THE MOON STILL HAS OUR FOOTPRINTS.';
}
tt.addEventListener('input', draw);
draw();
''',
   'caption': 'Each step multiplies the time. Everything we think of as permanent is '
              'gone within a few thousand years — and the longest-lasting thing we ever '
              'made is a set of footprints somewhere with no weather.'},

  {'type': 'scene', 'tone': 'rose', 'scene': 'overgrow',
   'h': 'Some of it recovers faster than you would think',
   'p': 'Places we have already abandoned fill with wildlife within decades. Not '
        'because they are clean, but because we are not there.'},

  {'type': 'text', 'h': 'What actually outlasts us',
   'p': ['Not the buildings. Plastic in the sediment, a thin layer of odd chemistry in '
         'the rock, and the radio signals already on their way out.',
         'And the footprints on the Moon, which have no wind or water to remove them '
         'and could plausibly still be there in <strong>ten million years</strong>.']},
 ],

 'zoomout': {'tone': 'forest',
   'text': 'Everything around you is being actively held in place. Stop holding, and '
           'the world does not end — it just carries on without the maintenance, and '
           'gets on perfectly well.'},
},

# ================================================================== 19
{
 'slug': 'why-are-ants-everywhere',
 'kicker': 'Life',
 'card_tone': 'solar', 'card_scene': 'colony',
 'featured': False,
 'title': 'Why are ants everywhere?',
 'teaser': 'Around twenty quadrillion of them. Together they weigh about as much as all wild birds and mammals put together.',
 'hero': {'tone': 'solar', 'scene': 'colony',
   'standfirst': 'Ants have been running the same business model for a hundred million '
                 'years, on every continent except Antarctica, and no single ant has '
                 'any idea how any of it works.'},

 'blocks': [
  {'type': 'text', 'h': 'The numbers are hard to hold',
   'p': ['The best estimate is about twenty thousand trillion ants alive right now. '
         'For every person, there are roughly two and a half million of them.',
         'Weighed together they come to something like <strong>all the wild birds and '
         'wild mammals on Earth, combined</strong>.']},

  {'type': 'scene', 'tone': 'forest', 'scene': 'colony',
   'h': 'A colony behaves like one animal',
   'p': 'Trails form, jobs get allocated, the nest gets repaired. Nobody is directing '
        'any of it.'},

  {'type': 'text', 'h': 'The queen is not in charge of anything',
   'p': ['She lays eggs. That is the whole job. She issues no orders and has no '
         'overview of the colony.',
         'Every decision comes from individual ants following simple local rules — '
         'mostly "follow the strongest smell" and "do the job nobody else is doing".']},

  {'type': 'turn', 'tone': 'ember',
   'text': 'No ant knows the plan. There is no plan. The colony still farms, builds, wages war and adapts.'},

  {'type': 'figure', 'tone': 'solar',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What a colony can do as it grows</title>
  <g id="nest"></g>
  <text class="f-label" x="360" y="60">COLONY SIZE</text>
  <text class="f-value" id="sizeTxt" x="360" y="96" style="font-size:26px">&#8212;</text>
  <text class="f-label" x="360" y="146">WHAT IT CAN DO</text>
  <text class="f-value" id="canTxt" x="360" y="180" style="font-size:19px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="360" y="232">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="n">Ants in the colony</label>
  <input type="range" id="n" min="1" max="70" step="1" value="20">
  <span class="readout" id="nOut">&#8212;</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var n = document.getElementById('n');
var COL = ['#FBBF24', '#FCD34D', '#A3E635', '#FB7185'];
var nest = document.getElementById('nest'), ants = [];
for (var i = 0; i < 70; i++) {
  var c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', 40 + (i % 10) * 27);
  c.setAttribute('cy', 60 + ((i / 10) | 0) * 30);
  c.setAttribute('r', 5);
  c.setAttribute('fill', COL[i % COL.length]);
  nest.appendChild(c);
  ants.push(c);
}

function draw() {
  var k = +n.value;
  var size = Math.round(Math.pow(10, k / 14));   // 1 up to about a million
  document.getElementById('nOut').textContent = size.toLocaleString('en-GB');
  document.getElementById('sizeTxt').textContent = size.toLocaleString('en-GB') + ' ants';
  document.getElementById('canTxt').textContent =
    size < 10 ? 'not much. it dies.' :
    size < 200 ? 'dig a nest, feed itself' :
    size < 5000 ? 'organised trails, division of labour' :
    size < 100000 ? 'farm fungus, herd aphids, raid rivals' :
                    'build bridges from its own bodies, run supply lines for miles';
  document.getElementById('noteTxt').textContent =
    size < 200 ? 'THE RULES EACH ANT FOLLOWS NEVER CHANGE' : 'SAME RULES. MORE ANTS. NEW BEHAVIOUR.';
  ants.forEach(function (a, i) {
    a.setAttribute('opacity', i < k ? .95 : .12);
  });
}
n.addEventListener('input', draw);
draw();
''',
   'caption': 'Nothing about the individual ant changes as you slide this. Only the '
              'number does — and past certain sizes, behaviours appear that no ant '
              'contains.'},

  {'type': 'scene', 'tone': 'nebula', 'scene': 'swarm',
   'h': 'They invented farming first',
   'p': 'Some ants have been growing fungus underground for fifty million years, '
        'weeding it, fertilising it and dosing it with antibiotics they carry on their '
        'bodies.'},

  {'type': 'text', 'h': 'Why this keeps coming up elsewhere',
   'p': ['Simple parts, local rules, no central control, complicated behaviour out the '
         'far end. That is ants, and it is also your brain cells, and flocks, and '
         'markets.',
         'The lesson ants keep teaching is that <strong>you do not need anyone in '
         'charge</strong> to get something that looks designed.']},
 ],

 'zoomout': {'tone': 'solar',
   'text': 'One ant is close to nothing — a few hundred thousand neurons and a handful '
           'of reflexes. A million of them, following the same reflexes, build '
           'something that farms. Nothing was added but number.'},
},

# ================================================================== 20
{
 'slug': 'why-time-slows-when-scared',
 'kicker': 'Mind',
 'card_tone': 'nebula', 'card_scene': 'timewarp',
 'featured': False,
 'title': 'Why does time slow down when you are scared?',
 'teaser': 'The crash felt like it lasted forever. Your brain was not running faster — it was recording more.',
 'hero': {'tone': 'nebula', 'scene': 'timewarp',
   'standfirst': 'Almost everyone who has been in an accident describes the same thing: '
                 'everything went slow. It is such a consistent report that somebody '
                 'eventually went and tested whether it was true.'},

 'blocks': [
  {'type': 'text', 'h': 'The obvious explanation',
   'p': ['If time seems to slow, your brain must be running faster — taking in more '
         'per second, like a high-speed camera.',
         'It is a good theory. It makes a clear prediction, which is what makes it '
         'testable.']},

  {'type': 'scene', 'tone': 'dusk', 'scene': 'timewarp',
   'h': 'Same stretch of time, two different speeds',
   'p': 'The top row is an ordinary minute. The bottom is the same minute, remembered '
        'after something frightening.'},

  {'type': 'text', 'h': 'So somebody dropped people off a tower',
   'p': ['Volunteers fell fifty metres backwards into a net, wearing a display '
         'flickering numbers just too fast to read normally.',
         'If perception really sped up, they would be able to read it during the fall. '
         '<strong>Nobody could.</strong> They were terrified, they reported the fall '
         'lasting far longer than it did, and they still could not read the display.']},

  {'type': 'turn', 'tone': 'ember',
   'text': 'Time did not slow down. Your memory got unusually detailed, and you read that density back as length.'},

  {'type': 'figure', 'tone': 'nebula',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Real duration against remembered duration</title>
  <text class="f-label" x="30" y="52">WHAT THE CLOCK SAYS</text>
  <rect x="30" y="66" width="600" height="26" rx="13" fill="rgba(255,255,255,.14)"/>
  <rect id="realBar" x="30" y="66" width="120" height="26" rx="13" fill="#22D3EE"/>
  <text class="f-value" id="realTxt" x="30" y="126" style="font-size:22px">&#8212;</text>

  <text class="f-label" x="30" y="176">WHAT YOU REMEMBER</text>
  <rect x="30" y="190" width="600" height="26" rx="13" fill="rgba(255,255,255,.14)"/>
  <rect id="feltBar" x="30" y="190" width="120" height="26" rx="13" fill="#F472B6"/>
  <text class="f-value" id="feltTxt" x="30" y="250" style="font-size:22px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="30" y="288">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="fear">How frightening it was</label>
  <input type="range" id="fear" min="0" max="100" step="1" value="10">
  <span class="readout" id="fearOut">&#8212;</span>
</div>''',
   'js': '''
var fear = document.getElementById('fear');
var REAL = 3;      // seconds, always

function draw() {
  var f = +fear.value / 100;
  document.getElementById('fearOut').textContent =
    f < .2 ? 'an ordinary moment' : f < .5 ? 'startling' : f < .8 ? 'frightening' : 'the worst kind';

  // duration is fixed; only the density of what got recorded changes
  var felt = REAL * (1 + f * 3.2);
  document.getElementById('realBar').setAttribute('width', 600 * REAL / 13);
  document.getElementById('feltBar').setAttribute('width', 600 * felt / 13);
  document.getElementById('realTxt').textContent = REAL.toFixed(1) + ' seconds';
  document.getElementById('feltTxt').textContent = felt.toFixed(1) + ' seconds';
  document.getElementById('noteTxt').textContent =
    f < .2 ? 'NOT MUCH WORTH STORING, SO NOT MUCH GETS STORED'
           : 'THE TOP BAR NEVER MOVES. IT NEVER DOES.';
}
fear.addEventListener('input', draw);
draw();
''',
   'caption': 'The cyan bar is the truth and it never changes. Only the pink one moves '
              '— and the pink one is the only one you have any access to.'},

  {'type': 'scene', 'tone': 'solar', 'scene': 'bloom',
   'h': 'The same trick runs your whole life',
   'p': 'A week somewhere new feels long looking back. A month of the same commute '
        'vanishes. You are not measuring time, you are measuring how much of it you '
        'kept.'},

  {'type': 'text', 'h': 'Which gives you something you can use',
   'p': ['You cannot slow time down. You can change how much of it gets recorded, and '
         'that is the thing you actually experience afterwards.',
         'New places, new people, anything unfamiliar. It is the only known way to '
         'make a year feel long.']},
 ],

 'zoomout': {'tone': 'nebula',
   'text': 'You have never once experienced time directly. You experience a '
           'reconstruction, assembled afterwards out of whatever your brain thought was '
           'worth keeping — and its filing decisions are the closest thing you have to '
           'a clock.'},
},

]
