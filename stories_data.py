# -*- coding: utf-8 -*-
"""Every story Context tells. One dict each; build.py does the rest.

Four stories, chosen because each one changes something a person does or
believes about their own body — and because each has a genuine reversal in
it. A reversal is what carries ten minutes of video. A fact alone does not.

    sleep    feeling fine and being fine come apart
    death    it is a sequence, not a moment
    immunity the symptoms are you, not the infection
    ageing   it is not wear and tear

Shape of a story:

    standfirst  the hook, in one breath
    blocks      the build, in order
    turn        the pivot. one line, set big
    zoomout     the landing

Blocks:
    text     white card, a heading and a couple of short paragraphs
    diagram  a labelled explanatory picture. static — you are reading it
    steps    a numbered checklist
    turn     the pivot, big type on full colour
    figure   the one thing per story you operate yourself

Only the hero panel carries ambient movement. Everything that explains
something holds still.
"""

STORIES = [

# ================================================================== 01
{
 'slug': 'why-do-we-sleep',
 'kicker': 'Sleep',
 'card_tone': 'dusk', 'thumb': 'sleep',
 'featured': True,
 'title': 'Why do we sleep?',
 'teaser': 'A third of your life spent unconscious and defenceless. What you get back for it, and what it costs when you skip it.',
 'takeaway': 'Why you feel fine on six hours and are not fine on six hours.',
 'hero': {'tone': 'dusk', 'scene': 'night',
   'standfirst': 'Lying still and unaware for eight hours is close to the most dangerous '
                 'thing an animal can do. Every animal with a brain does it anyway. '
                 'Whatever sleep buys, it is worth being eaten over.'},

 'blocks': [
  {'type': 'text', 'h': 'It is far too expensive to be an accident',
   'p': ['While asleep you cannot eat, defend yourself or watch for anything. If sleep '
         'were optional, some animal would have dropped it and out-competed the rest.',
         'None has. Not one. Whatever is happening up there, <strong>it cannot be done '
         'while the lights are on</strong>.']},

  {'type': 'diagram', 'name': 'sleep_architecture',
   'caption': 'A night is not one long blank. You cycle roughly every ninety minutes, '
              'and the two halves of the night do different jobs.'},

  {'type': 'text', 'h': 'The brain is rinsed while you are out',
   'p': ['During deep sleep the gaps between brain cells widen and fluid is pushed '
         'through, carrying out waste built up during the day.',
         'It works far better asleep than awake — a good reason for the brain to do it '
         'while you are not using it.']},

  {'type': 'diagram', 'name': 'sleep_jobs',
   'caption': 'Deep sleep repairs. REM files. Cut the night short and you lose the '
              'second one first, because dreaming loads the end of the night.'},

  {'type': 'scene', 'tone': 'void', 'scene': 'mind',
   'h': 'Nothing about the brain is idle at night',
   'p': 'It is running a maintenance schedule it cannot run while you are using it — which is a very different thing from being switched off.'},

  {'type': 'turn', 'tone': 'deepsea',
   'text': 'Sleep is not the brain switching off. It is maintenance that cannot run while you are using the machine.'},

  {'type': 'text', 'h': 'And here is the part that catches people',
   'p': ['Lose sleep steadily and your performance drops and stays down. Your <em>sense</em> '
         'of how you are doing recovers within a couple of days.',
         'So people running on five hours reliably report feeling fine. Measured, they '
         'are not fine. <strong>The gauge is broken, not the engine.</strong>']},

  {'type': 'diagram', 'name': 'sleep_debt',
   'caption': 'Everything that matters falls off below about seven hours — and the one '
              'thing that does not fall off is your confidence that you are coping.'},

  {'type': 'figure', 'tone': 'dusk',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">How sleep debt accumulates over a working week</title>
  <line class="f-faint" x1="60" y1="230" x2="620" y2="230"/>
  <g id="bars"></g>
  <text class="f-label" x="60" y="256">MON</text>
  <text class="f-label" x="620" y="256" text-anchor="end">SUN</text>
  <text class="f-label" x="60" y="40">SLEEP DEBT BY THE END OF THE WEEK</text>
  <text class="f-value" id="debtTxt" x="60" y="76" style="font-size:28px">&#8212;</text>
  <text class="f-label" id="noteTxt" x="60" y="288">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="hrs">Hours a night</label>
  <input type="range" id="hrs" min="4" max="9" step="0.5" value="6">
  <span class="readout" id="hrsOut">6 hours</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var hrs = document.getElementById('hrs'), box = document.getElementById('bars');
var NEED = 8;

function draw() {
  var h = +hrs.value;
  document.getElementById('hrsOut').textContent = h + ' hours';
  box.textContent = '';
  var short = Math.max(0, NEED - h);
  for (var d = 0; d < 7; d++) {
    var debt = short * (d + 1);
    var bh = Math.min(160, debt * 16);
    var r = document.createElementNS(NS, 'rect');
    r.setAttribute('x', 60 + d * 80);
    r.setAttribute('y', 230 - bh);
    r.setAttribute('width', 52);
    r.setAttribute('height', Math.max(bh, 2));
    r.setAttribute('rx', 8);
    r.setAttribute('fill', debt > 10 ? '#FB7185' : debt > 5 ? '#FBBF24' : '#34D399');
    box.appendChild(r);
  }
  var total = short * 7;
  document.getElementById('debtTxt').textContent =
    total === 0 ? 'none' : total.toFixed(1) + ' hours short';
  document.getElementById('noteTxt').textContent =
    total === 0 ? 'YOU ARE STARTING EACH DAY WHOLE' :
    total < 7 ? 'RECOVERABLE WITH A COUPLE OF GOOD NIGHTS' :
    total < 14 ? 'THIS IS ROUGHLY A WHOLE NIGHT LOST, EVERY WEEK' :
                 'AT THIS RATE YOU ARE PERMANENTLY IMPAIRED AND WILL NOT FEEL IT';
}
hrs.addEventListener('input', draw);
draw();
''',
   'caption': 'Debt adds up night after night; it does not reset on its own. Slide to '
              'six hours — the most common answer people give — and see where the week '
              'ends up.'},

  {'type': 'steps', 'tone': 'solar', 'h': 'What actually works',
   'items': [
     {'h': 'A fixed wake time', 'p': 'More useful than a fixed bedtime. The body clock anchors to when light arrives, not when you switch off.'},
     {'h': 'Light in the morning', 'p': 'Ten minutes outdoors shortly after waking does more for the clock than anything you do at night.'},
     {'h': 'Stop counting the good nights', 'p': 'One long lie-in does not clear a week of debt. Consistency beats catching up.'},
     {'h': 'Treat caffeine as long-acting', 'p': 'Half of a 3pm coffee is still in you at 9pm, quietly shortening the deep half of the night.'}]},
 ],

 'zoomout': {'tone': 'dusk',
   'text': 'You will spend around twenty-six years of your life asleep. Not lost time — '
           'it is the maintenance window that makes the other fifty-odd years work at '
           'all. It is also the one health decision available to everybody, for free, '
           'tonight.'},
},

# ================================================================== 02
{
 'slug': 'what-happens-when-you-die',
 'kicker': 'Death',
 'card_tone': 'ember', 'thumb': 'death',
 'featured': True,
 'title': 'What actually happens when you die?',
 'teaser': 'Not a switch flicking off. A shutdown that runs in a specific order and takes hours — which is why transplants are possible at all.',
 'takeaway': 'What the order of shutdown means for donation, and for how we define death.',
 'hero': {'tone': 'ember', 'scene': 'fading',
   'standfirst': 'We talk about death as a moment: a line crossed, a light going out. '
                 'Biologically there is no line. There is a sequence, it runs in a '
                 'fixed order, and it takes much longer than almost anyone expects.'},

 'blocks': [
  {'type': 'text', 'h': 'The heart stops. Almost nothing else does.',
   'p': ['Your brain has roughly ten seconds of oxygen left in it once circulation ends. '
         'That part is quick, and it is the part everyone pictures.',
         'Everything else carries on. Your cells have no way of knowing anything has '
         'happened. They have fuel and a job, and they keep doing it for '
         '<strong>minutes to hours</strong>.']},

  {'type': 'diagram', 'name': 'death_sequence',
   'caption': 'The order matters more than the moment. Red is where nothing can be '
              'recovered; teal is where things still can.'},

  {'type': 'scene', 'tone': 'void', 'scene': 'cell',
   'h': 'Your cells never get the message',
   'p': 'They have fuel and a job, and no way of knowing that the body they belong to has stopped. Most of them carry on for hours.'},

  {'type': 'turn', 'tone': 'solar',
   'text': 'You do not die all at once. Different parts of you stop at different times, over hours.'},

  {'type': 'text', 'h': 'Which is why transplant medicine exists',
   'p': ['A donated heart can be restarted in someone else hours after its owner died. '
         'A cornea works after a week or more.',
         'If death were a single instant, <strong>none of that would be possible</strong>. '
         'The whole field lives inside the gap between the first thing stopping and the '
         'last.']},

  {'type': 'diagram', 'name': 'death_viability',
   'caption': 'The brain is the outlier. Everything else has a usable window, and the '
              'window is measured in hours or days rather than seconds.'},

  {'type': 'text', 'h': 'So the definition had to be rewritten',
   'p': ['For thousands of years, death meant the heart had stopped. Then we learned to '
         'restart hearts, and people came back.',
         'The line moved to the brain — the one part that cannot be restarted, replaced '
         'or kept going by a machine.']},

  {'type': 'diagram', 'name': 'death_definitions',
   'caption': 'This is why "brain death" and "cardiac death" are different things in a '
              'hospital, and why only one of them is treated as final.'},

  {'type': 'figure', 'tone': 'ember',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">What is still viable at a given time after the heart stops</title>
  <g id="organs"></g>
  <line class="f-faint" x1="30" y1="256" x2="630" y2="256"/>
  <circle id="mark" cx="30" cy="256" r="6" fill="#FCD34D"/>
  <text class="f-label" x="30" y="282">HEART STOPS</text>
  <text class="f-label" x="630" y="282" text-anchor="end">36 HOURS</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="mins">Time since the heart stopped</label>
  <input type="range" id="mins" min="0" max="2160" step="5" value="0">
  <span class="readout" id="minsOut">0 min</span>
</div>''',
   'js': '''
var NS = 'http://www.w3.org/2000/svg';
var mins = document.getElementById('mins');
// roughly how long each tissue stays transplantable without circulation
var ORGANS = [
  { n: 'Brain',   life: 5,    col: '#FB7185' },
  { n: 'Heart',   life: 300,  col: '#F472B6' },
  { n: 'Lungs',   life: 420,  col: '#FBBF24' },
  { n: 'Liver',   life: 720,  col: '#FCD34D' },
  { n: 'Kidneys', life: 1800, col: '#A3E635' },
  { n: 'Cornea',  life: 2160, col: '#22D3EE' }
];
var host = document.getElementById('organs'), rows = [];
ORGANS.forEach(function (o, i) {
  var g = document.createElementNS(NS, 'g'), y = 42 + i * 34;
  g.innerHTML =
    '<text x="30" y="' + (y + 5) + '" class="f-label">' + o.n.toUpperCase() + '</text>' +
    '<rect x="150" y="' + (y - 10) + '" width="390" height="18" rx="9" fill="rgba(255,255,255,.12)"/>' +
    '<rect x="150" y="' + (y - 10) + '" width="390" height="18" rx="9" fill="' + o.col + '"/>' +
    '<text x="558" y="' + (y + 5) + '" class="f-label">usable</text>';
  host.appendChild(g);
  rows.push({ o: o, bar: g.children[2], lab: g.children[3] });
});

function draw() {
  var m = +mins.value;
  document.getElementById('minsOut').textContent =
    m < 60 ? m + ' min' : (m / 60).toFixed(1) + ' hours';
  document.getElementById('mark').setAttribute('cx', 30 + (m / 2160) * 600);
  rows.forEach(function (r) {
    var left = Math.max(0, 1 - m / r.o.life);
    r.bar.setAttribute('width', 390 * left);
    r.lab.textContent = left > 0 ? 'usable' : 'gone';
    r.lab.setAttribute('opacity', left > 0 ? 1 : .4);
  });
}
mins.addEventListener('input', draw);
draw();
''',
   'caption': 'Drag forward. The brain is gone before the bar has visibly moved; a '
              'cornea is still viable a day later. That spread is the whole reason organ '
              'donation works.'},
 ],

 'zoomout': {'tone': 'ember',
   'text': 'Nothing about you is destroyed. Every atom carries on and ends up somewhere '
           'else. What ends is the arrangement — and the arrangement was always the '
           'temporary part. Knowing the order it comes apart in is also, very '
           'practically, why one death can leave several people alive.'},
},

# ================================================================== 03
{
 'slug': 'the-war-inside-you',
 'kicker': 'Immunity',
 'card_tone': 'deepsea', 'thumb': 'immune',
 'featured': True,
 'title': 'The war going on inside you right now',
 'teaser': 'Everything you hate about being ill is your own body fighting. The infection does surprisingly little of it.',
 'takeaway': 'What a fever is doing, and why a sore arm after a jab is the point.',
 'hero': {'tone': 'deepsea', 'scene': 'cell',
   'standfirst': 'While you read this, something inside you is finding, identifying and '
                 'killing invaders — thousands of them — and you will not notice a '
                 'single one of those fights.'},

 'blocks': [
  {'type': 'text', 'h': 'Almost nothing gets past the first layer',
   'p': ['Skin, mucus, stomach acid and tears stop the overwhelming majority of what '
         'lands on you, constantly, without any drama.',
         'You only ever find out about the failures. <strong>Every illness you have had '
         'was an exception</strong>, not the rule.']},

  {'type': 'diagram', 'name': 'immune_layers',
   'caption': 'Each layer only deals with what got past the one before it. By the time '
              'the third is involved, you feel ill.'},

  {'type': 'text', 'h': 'The first responders do not aim',
   'p': ['Break the skin and blunt, fast cells arrive within minutes and swallow anything '
         'without the right password. No targeting, no thinking.',
         'They also open blood vessels and make the area leak fluid, which is what '
         'swelling is. The pain that follows is deliberate: it stops you using the part '
         'that needs to heal.']},

  {'type': 'scene', 'tone': 'void', 'scene': 'cell',
   'h': 'Thousands of these are settled every day without you',
   'p': 'You are only ever aware of the exceptions — the handful that got far enough to need the expensive machinery.'},

  {'type': 'turn', 'tone': 'rose',
   'text': 'Every symptom you hate is your own body fighting. Winning is what feels awful.'},

  {'type': 'diagram', 'name': 'immune_battle',
   'caption': 'You feel worst around day three — not when the invaders are winning, but '
              'when your own response is at full volume.'},

  {'type': 'text', 'h': 'Then the specialists arrive, and they remember',
   'p': ['If the blunt cells cannot finish it, they carry a piece of the enemy away and '
         'show it around until they find the one cell that recognises it. That cell '
         'copies itself into an army shaped for this exact invader.',
         'It takes days — which is why you stay ill for a week. And afterwards, some of '
         'those cells stay behind for <strong>decades</strong>.']},

  {'type': 'diagram', 'name': 'immune_vaccine',
   'caption': 'A vaccine is not medicine you take when ill. It is that rehearsal, run in '
              'advance, without the danger.'},

  {'type': 'figure', 'tone': 'deepsea',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Invaders and defences over the days after an infection</title>
  <line class="f-faint" x1="50" y1="230" x2="620" y2="230"/>
  <path id="germLine" class="f-line" d="" stroke="#FB7185" stroke-dasharray="7 5"/>
  <path id="immLine" class="f-line" d="" stroke="#22D3EE"/>
  <line id="cursor" class="f-faint" x1="50" y1="50" x2="50" y2="230"/>
  <text class="f-label" x="50" y="42">INVADERS (DASHED) &#183; YOUR DEFENCES (SOLID)</text>
  <text class="f-label" x="50" y="254">INFECTED</text>
  <text class="f-label" x="620" y="254" text-anchor="end">DAY 10</text>
  <text class="f-value" id="feelTxt" x="50" y="288" style="font-size:19px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="day">Day</label>
  <input type="range" id="day" min="0" max="100" step="1" value="0">
  <span class="readout" id="dayOut">0.0</span>
</div>''',
   'js': '''
var day = document.getElementById('day');

function germs(t) {
  return Math.max(0, Math.exp(-Math.pow((t - 2.4) / 1.9, 2)) * .95 - (t > 5 ? (t - 5) * .09 : 0));
}
function immune(t) { return Math.min(1, .07 + Math.pow(t / 10, 1.5) * 1.3); }

function path(fn) {
  var d = '';
  for (var i = 0; i <= 100; i++) {
    d += (i ? 'L' : 'M') + (50 + (i / 100) * 570).toFixed(1) + ' ' + (230 - fn(i / 10) * 170).toFixed(1);
  }
  return d;
}
document.getElementById('germLine').setAttribute('d', path(germs));
document.getElementById('immLine').setAttribute('d', path(immune));

function draw() {
  var t = +day.value / 10;
  document.getElementById('dayOut').textContent = t.toFixed(1);
  var x = 50 + (+day.value / 100) * 570;
  document.getElementById('cursor').setAttribute('x1', x);
  document.getElementById('cursor').setAttribute('x2', x);
  document.getElementById('feelTxt').textContent =
    t < .5 ? 'The barrier is broken. You feel nothing yet.' :
    t < 2  ? 'The first responders arrive. Warm, sore, swollen.' :
    t < 4  ? 'Peak misery — and this is your side of the fight, not theirs.' :
    t < 7  ? 'The specialists land. The tide turns.' :
             'Almost over. Some of these cells will remember this for decades.';
}
day.addEventListener('input', draw);
draw();
''',
   'caption': 'Watch the two lines. The moment you feel worst is not where the pink line '
              'peaks — it is where the blue one is climbing hardest.'},
 ],

 'zoomout': {'tone': 'deepsea',
   'text': 'You have never had to think about any of this. Something inside you has been '
           'making life-or-death identifications every second since the day you were '
           'born, and has never once asked you for a decision. Understanding it changes '
           'what you make of a fever — and what you make of a sore arm after a jab.'},
},

# ================================================================== 04
{
 'slug': 'why-do-we-age',
 'kicker': 'Ageing',
 'card_tone': 'nebula', 'thumb': 'age',
 'featured': True,
 'title': 'Why do we get old?',
 'teaser': 'Not wear and tear — you are rebuilt constantly. Something else is going on, and some of it you can change.',
 'takeaway': 'Which interventions actually hold up, ranked by evidence rather than hype.',
 'hero': {'tone': 'nebula', 'scene': 'dividing',
   'standfirst': 'A car wears out because nothing repairs it. You are repaired every '
                 'day by trillions of cells whose entire job is maintenance. So the '
                 'obvious explanation cannot be the right one.'},

 'blocks': [
  {'type': 'text', 'h': 'You are rebuilt all the time',
   'p': ['Your gut lining is days old. Your skin is weeks old. Even your skeleton '
         'replaces itself over about a decade.',
         'If ageing were simply things wearing out, constant rebuilding would hold it '
         'off more or less forever. <strong>It plainly does not.</strong>']},

  {'type': 'diagram', 'name': 'age_hallmarks',
   'caption': 'Ageing is not one process. It is several specific ones — which is exactly '
              'why it is the kind of problem that can be worked on at all.'},

  {'type': 'text', 'h': 'And the repair crew ages too',
   'p': ['Worn-out cells do not always leave quietly. Many stop working, refuse to die, '
         'and start leaking signals that inflame the tissue around them.',
         'So damage accumulates while the ability to fix it declines. Those two lines '
         'crossing is a decent working definition of getting old.']},

  {'type': 'diagram', 'name': 'age_curves',
   'caption': 'Nothing dramatic happens at any particular birthday. Two curves simply '
              'cross, somewhere in mid-life, and after that the balance runs the other way.'},

  {'type': 'scene', 'tone': 'void', 'scene': 'cell',
   'h': 'Every copy is very slightly worse than the last',
   'p': 'Not catastrophically. Just enough that the errors outrun the corrections, given long enough — and nothing is selecting against it.'},

  {'type': 'turn', 'tone': 'solar',
   'text': 'Evolution has no reason to keep you in good repair after you have had children. Ageing is where it stops paying.'},

  {'type': 'text', 'h': 'Which is why some animals barely do it',
   'p': ['A bowhead whale can pass two hundred. Some tortoises show almost no rise in '
         'death rate with age at all.',
         'Where staying alive longer pays off, evolution buys better repair. Ageing is '
         'not a law of physics — it is <strong>a maintenance budget</strong>.']},

  {'type': 'figure', 'tone': 'nebula',
   'svg': '''<svg viewBox="0 0 660 300" role="img" aria-labelledby="figTitle">
  <title id="figTitle">Damage against repair capacity across a lifetime</title>
  <line class="f-faint" x1="50" y1="230" x2="620" y2="230"/>
  <path id="dmg" class="f-line" d="" stroke="#FB7185"/>
  <path id="rep" class="f-line" d="" stroke="#34D399"/>
  <line id="cursor" class="f-faint" x1="50" y1="46" x2="50" y2="230"/>
  <text class="f-label" x="50" y="40">DAMAGE (PINK) &#183; REPAIR (GREEN)</text>
  <text class="f-label" x="50" y="254">BIRTH</text>
  <text class="f-label" x="620" y="254" text-anchor="end">100</text>
  <text class="f-value" id="stateTxt" x="50" y="288" style="font-size:19px">&#8212;</text>
</svg>''',
   'controls': '''<div class="control">
  <label for="age">Age</label>
  <input type="range" id="age" min="0" max="100" step="1" value="25">
  <span class="readout" id="ageOut">25</span>
</div>''',
   'js': '''
var age = document.getElementById('age');
function damage(a) { return Math.min(1, Math.pow(a / 100, 1.9) * 1.35); }
function repair(a) { return Math.max(.05, 1 - Math.pow(a / 100, 1.6) * 1.15); }

function path(fn) {
  var d = '';
  for (var i = 0; i <= 100; i++) {
    d += (i ? 'L' : 'M') + (50 + i * 5.7).toFixed(1) + ' ' + (230 - fn(i) * 175).toFixed(1);
  }
  return d;
}
document.getElementById('dmg').setAttribute('d', path(damage));
document.getElementById('rep').setAttribute('d', path(repair));

function draw() {
  var a = +age.value;
  document.getElementById('ageOut').textContent = a;
  var x = 50 + a * 5.7;
  document.getElementById('cursor').setAttribute('x1', x);
  document.getElementById('cursor').setAttribute('x2', x);
  var d = damage(a), r = repair(a);
  document.getElementById('stateTxt').textContent =
    r > d + .35 ? 'Repair is winning comfortably. You barely notice a bad week.' :
    r > d       ? 'Still ahead, but the gap is closing.' :
    r > d - .3  ? 'The lines have crossed. This is what ageing feels like.' :
                  'Damage now accumulates faster than anything can clear it.';
}
age.addEventListener('input', draw);
draw();
''',
   'caption': 'Drag through a lifetime. The crossing is not a cliff — it is the point '
              'after which recovery from everything takes measurably longer.'},

  {'type': 'diagram', 'name': 'age_levers',
   'caption': 'Ranked by strength of evidence rather than by how much attention each one '
              'gets. The unglamorous ones win, and they have kept winning for decades.'},
 ],

 'zoomout': {'tone': 'nebula',
   'text': 'Ageing looks less like a law of nature and more like a maintenance contract '
           'that runs out. That does not make it easy to renegotiate. It does mean the '
           'question "what actually helps" has real answers — and that most of them are '
           'available to you now, for nothing.'},
},

]

# ------------------------------------------------------------------ the library
# Stories 5-50 live in library.py as briefs and are expanded here. They are
# shorter than the flagship four by design; the four above carry hand-composed
# diagrams and interactive figures, the rest carry the same six beats at a
# tighter length. Both are held to the standard in STYLE.md.

from library import BRIEFS as _BRIEFS, expand as _expand

LIBRARY_STORIES = []
LIBRARY_PAPERS = []
for _i, _br in enumerate(_BRIEFS):
    _s, _p = _expand(_br, _i)
    LIBRARY_STORIES.append(_s)
    LIBRARY_PAPERS.append(_p)

# Twelve stories share the `mind` scene and nine share `cell`, so the variant
# picked by hand in a brief was never going to be unique. Assign it here
# instead: every story gets its own index within its scene, which the
# illustrator turns into its own palette rotation and its own framing. No two
# banners on the site are the same picture.
_used = {}
for _s in LIBRARY_STORIES:
    _sc = _s['hero']['scene']
    _used[_sc] = _used.get(_sc, 0) + 1
    _s['hero']['var'] = _used[_sc]
    for _b in _s['blocks']:
        if _b['type'] == 'scene':
            _b['var'] = _used[_sc] + 7

STORIES = STORIES + LIBRARY_STORIES
