# -*- coding: utf-8 -*-
"""Labelled explanatory diagrams.

Different job from illustrate.py. That file makes atmosphere for the hero
panels; this one makes the pictures that actually teach. Every diagram here
is hand-composed for one specific idea, drawn flat and in colour, and
labelled — leader lines, captions on the parts, a legend where two things
need telling apart.

They do not animate. A diagram you are reading should hold still.

They sit on light cards, because dark panels are for atmosphere and labelled
teaching material reads better as ink on paper.
"""

# Diagram palette. Saturated enough to separate parts at a glance, dark
# enough that the labels on top of them stay legible.
C = {
    'ink':    '#101828',
    'muted':  '#5A6875',
    'line':   '#CBD5E1',
    'paper':  '#FFFFFF',
    'shade':  '#F1F5F9',
    'blue':   '#2563EB',
    'cyan':   '#0891B2',
    'teal':   '#0D9488',
    'green':  '#059669',
    'lime':   '#65A30D',
    'amber':  '#D97706',
    'orange': '#EA580C',
    'red':    '#DC2626',
    'rose':   '#E11D48',
    'pink':   '#DB2777',
    'violet': '#7C3AED',
    'indigo': '#4F46E5',
}

VB_W, VB_H = 940, 560


# ---------------------------------------------------------------- helpers

def _svg(body, w=VB_W, h=VB_H, title=''):
    t = f'<title>{title}</title>' if title else ''
    return (f'<svg class="dia" viewBox="0 0 {w} {h}" role="img" '
            f'preserveAspectRatio="xMidYMid meet">{t}{body}</svg>')


def label(x, y, text, size=15, col=None, anchor='start', weight=600):
    col = col or C['ink']
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{col}" '
            f'font-size="{size}" font-weight="{weight}" '
            f'font-family="Gabarito, system-ui, sans-serif">{text}</text>')


def note(x, y, text, size=13, col=None, anchor='start'):
    col = col or C['muted']
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{col}" '
            f'font-size="{size}" font-family="Source Sans 3, system-ui, sans-serif">{text}</text>')


def leader(x1, y1, x2, y2, col=None):
    col = col or C['line']
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="1.5" '
            f'fill="none" stroke-dasharray="3 3"/>'
            f'<circle cx="{x1}" cy="{y1}" r="3.5" fill="{col}"/>')


def tag(x, y, text, col, w=None):
    """A small filled pill — used to name a coloured part."""
    w = w or (len(text) * 7.6 + 22)
    return (f'<g><rect x="{x}" y="{y - 13}" width="{w:.0f}" height="24" rx="12" fill="{col}"/>'
            f'{label(x + w / 2, y + 5, text, 12.5, "#fff", "middle", 700)}</g>')


def bar(x, y, w, h, frac, col, bg=None):
    bg = bg or C['shade']
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{bg}"/>'
            f'<rect x="{x}" y="{y}" width="{max(w * frac, h):.0f}" height="{h}" rx="{h/2}" fill="{col}"/>')


def panel(x, y, w, h, col, op=.1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{col}" opacity="{op}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="none" '
            f'stroke="{col}" stroke-width="1.5" opacity=".45"/>')


def cell(cx, cy, r, col, nucleus=None, spikes=0):
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity=".22"/>'
    if spikes:
        for i in range(spikes):
            import math
            a = (i / spikes) * math.tau
            out += (f'<line x1="{cx + math.cos(a) * r:.0f}" y1="{cy + math.sin(a) * r:.0f}" '
                    f'x2="{cx + math.cos(a) * r * 1.3:.0f}" y2="{cy + math.sin(a) * r * 1.3:.0f}" '
                    f'stroke="{col}" stroke-width="3" stroke-linecap="round"/>')
    out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="3.5"/>'
    if nucleus:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r * .42:.0f}" fill="{nucleus}"/>'
    return out


def arrow(x1, y1, x2, y2, col, width=3):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - math.cos(a) * 10, y2 - math.sin(a) * 10
    head = (f'<path d="M{x2} {y2} L{hx + math.sin(a) * 6:.0f} {hy - math.cos(a) * 6:.0f} '
            f'L{hx - math.sin(a) * 6:.0f} {hy + math.cos(a) * 6:.0f} Z" fill="{col}"/>')
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.0f}" y2="{hy:.0f}" stroke="{col}" '
            f'stroke-width="{width}" stroke-linecap="round"/>{head}')


# ================================================================ SLEEP

def sleep_architecture():
    """A night of sleep as a hypnogram, with the stages named."""
    stages = [('Awake', C['amber']), ('REM', C['pink']), ('Light', C['cyan']),
              ('Deep', C['indigo'])]
    top, rowh, x0, x1 = 90, 74, 130, 880
    out = [label(40, 46, 'One night of sleep', 22),
           note(40, 68, 'Four to five cycles. Deep sleep loads the first half; dreaming loads the second.')]

    for i, (name, col) in enumerate(stages):
        y = top + i * rowh
        out.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{rowh - 14}" rx="10" '
                   f'fill="{col}" opacity=".08"/>')
        out.append(label(40, y + 26, name, 14, col))

    # the trace: down into deep early, more REM later
    nights = [(0, 0), (.04, 2), (.1, 3), (.17, 3), (.22, 2), (.26, 1),
              (.3, 2), (.36, 3), (.42, 3), (.46, 2), (.5, 1),
              (.55, 2), (.6, 2.4), (.65, 2), (.7, 1), (.74, 0),
              (.78, 1), (.83, 2), (.88, 1.6), (.93, 1), (1, 0)]
    pts = []
    for f, st in nights:
        pts.append((x0 + f * (x1 - x0), top + st * rowh + (rowh - 14) / 2))
    d = 'M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{C["ink"]}" stroke-width="3.5" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')

    # mark one full cycle
    out.append(f'<rect x="{x0 + .04 * (x1 - x0):.0f}" y="{top - 16}" '
               f'width="{.26 * (x1 - x0):.0f}" height="{4 * rowh - 4}" rx="12" '
               f'fill="none" stroke="{C["violet"]}" stroke-width="2" stroke-dasharray="6 5"/>')
    out.append(tag(x0 + .05 * (x1 - x0), top - 26, 'one cycle, about 90 minutes', C['violet']))

    out.append(note(x0, 500, 'Asleep', 13))
    out.append(note(x1, 500, '8 hours later', 13, anchor='end'))
    out.append(f'<line x1="{x0}" y1="480" x2="{x1}" y2="480" stroke="{C["line"]}" stroke-width="1.5"/>')
    # where dreaming concentrates
    out.append(f'<rect x="{x0 + .6 * (x1 - x0):.0f}" y="472" width="{.4 * (x1 - x0):.0f}" '
               f'height="16" rx="8" fill="{C["pink"]}" opacity=".3"/>')
    out.append(note(x0 + .78 * (x1 - x0), 528, 'most dreaming happens here', 13, C['pink'], 'middle'))
    return _svg(''.join(out), title='A night of sleep, showing four cycles through the sleep stages')


def sleep_jobs():
    """What each part of the night is for."""
    items = [
        ('Deep sleep', C['indigo'], 'The brain is rinsed', 'Gaps between brain cells widen and fluid flushes the day’s waste out.'),
        ('Deep sleep', C['cyan'], 'The body is repaired', 'Growth hormone peaks. Tissue is rebuilt and the immune system is restocked.'),
        ('REM sleep', C['pink'], 'The day is filed', 'Memories are replayed, sorted and attached to things you already knew.'),
        ('REM sleep', C['violet'], 'Feelings are defused', 'Difficult memories are re-stored with less of their emotional charge.'),
    ]
    out = [label(40, 46, 'What the night is actually for', 22),
           note(40, 68, 'Two different jobs, done at two different times. Cut the night short and you lose the second one first.')]
    for i, (stage, col, head, body) in enumerate(items):
        x = 40 + (i % 2) * 460
        y = 110 + (i // 2) * 205
        out.append(panel(x, y, 420, 175, col))
        out.append(tag(x + 24, y + 40, stage, col))
        out.append(label(x + 24, y + 92, head, 18))
        # wrap by hand: two short lines
        words, line, lines = body.split(), '', []
        for wd in words:
            if len(line + wd) > 42:
                lines.append(line); line = ''
            line += wd + ' '
        lines.append(line)
        for j, ln in enumerate(lines[:3]):
            out.append(note(x + 24, y + 122 + j * 21, ln.strip(), 14))
    return _svg(''.join(out), title='The four jobs sleep does, split between deep sleep and REM')


def sleep_debt():
    """What falls over as sleep is cut."""
    rows = [('Reaction time', C['blue']), ('Memory forming', C['violet']),
            ('Emotional control', C['pink']), ('Immune response', C['green'])]
    hours = [4, 5, 6, 7, 8]
    out = [label(40, 46, 'What breaks as the night gets shorter', 22),
           note(40, 68, 'Each bar is performance against a full night. The catch is that how you feel recovers long before performance does.')]
    x0, w = 250, 560
    for i, (name, col) in enumerate(rows):
        y = 120 + i * 74
        out.append(label(40, y + 22, name, 15))
        for j, hr in enumerate(hours):
            frac = min(1, (hr / 8) ** 1.7)
            bw = w / len(hours) - 12
            out.append(bar(x0 + j * (w / len(hours)), y, bw, 30, frac, col))
            if i == 0:
                out.append(note(x0 + j * (w / len(hours)) + bw / 2, y - 14, f'{hr}h', 13, anchor='middle'))
    out.append(f'<rect x="{x0 - 8}" y="106" width="{w / len(hours):.0f}" height="{4 * 74:.0f}" '
               f'rx="14" fill="{C["red"]}" opacity=".07"/>')
    out.append(note(x0 + 46, 440, 'four hours', 13, C['red'], 'middle'))
    out.append(note(x0 + w - 50, 440, 'a full night', 13, C['green'], 'middle'))
    out.append(note(40, 500, 'People running on five hours consistently rate themselves as unaffected. They are measurably not.', 14, C['ink']))
    return _svg(''.join(out), title='Performance across four measures at different amounts of sleep')


# ================================================================ DEATH

def death_sequence():
    """The order things stop in, on a timeline."""
    events = [
        (.02, 'Heart stops', C['red'], 'Circulation ends. Nothing else has noticed yet.'),
        (.08, '10 seconds', C['rose'], 'The brain runs out of oxygen. Consciousness goes.'),
        (.28, '4-6 minutes', C['orange'], 'Brain cells begin to die without oxygen.'),
        (.52, 'Hours', C['amber'], 'Most other tissue is still alive and usable.'),
        (.82, '24+ hours', C['teal'], 'Skin and cornea are still viable for transplant.'),
    ]
    x0, x1, y = 70, 880, 250
    out = [label(40, 46, 'Death is a sequence, not a moment', 22),
           note(40, 68, 'Different parts of the body stop at very different times. This is the order they go in.')]
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{C["line"]}" stroke-width="4" stroke-linecap="round"/>')
    grad = (f'<defs><linearGradient id="dseq" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{C["red"]}"/><stop offset=".5" stop-color="{C["amber"]}"/>'
            f'<stop offset="1" stop-color="{C["teal"]}"/></linearGradient></defs>')
    out.insert(0, grad)
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#dseq)" stroke-width="4" stroke-linecap="round"/>')
    for i, (f, name, col, desc) in enumerate(events):
        x = x0 + f * (x1 - x0)
        up = i % 2 == 0
        ty = y - 40 if up else y + 40
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="11" fill="{col}"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="19" fill="{col}" opacity=".22"/>')
        out.append(f'<line x1="{x:.0f}" y1="{y + (-19 if up else 19)}" x2="{x:.0f}" y2="{ty + (12 if up else -12)}" '
                   f'stroke="{col}" stroke-width="2"/>')
        anchor = 'middle'
        out.append(label(x, ty + (0 if up else 6), name, 16, col, anchor))
        words, line, lines = desc.split(), '', []
        for wd in words:
            if len(line + wd) > 26:
                lines.append(line); line = ''
            line += wd + ' '
        lines.append(line)
        for j, ln in enumerate(lines[:2]):
            oy = ty - 44 + j * 19 if up else ty + 28 + j * 19
            out.append(note(x, oy, ln.strip(), 13, anchor=anchor))
    out.append(note(x0, 500, 'Red is where nothing can be recovered. Teal is where things still can.', 14, C['ink']))
    return _svg(''.join(out), title='Timeline of what stops working, and when, after the heart stops')


def death_viability():
    """Why transplants are possible at all."""
    organs = [('Brain', .01, C['rose'], 'minutes'), ('Heart', .17, C['red'], '4-6 hours'),
              ('Lungs', .25, C['orange'], '6-8 hours'), ('Liver', .5, C['amber'], '12 hours'),
              ('Kidneys', .75, C['lime'], '24-36 hours'), ('Cornea', 1.0, C['teal'], 'up to 14 days')]
    out = [label(40, 46, 'How long each part stays usable', 22),
           note(40, 68, 'If death were a single instant, none of this would be possible. Transplant medicine lives in this gap.')]
    x0, w = 210, 560
    for i, (name, frac, col, when) in enumerate(organs):
        y = 116 + i * 62
        out.append(label(40, y + 22, name, 16))
        out.append(bar(x0, y, w, 32, frac, col))
        out.append(note(x0 + w + 18, y + 22, when, 14, col))
    out.append(f'<rect x="{x0 - 10}" y="106" width="26" height="{6 * 62 - 10}" rx="12" '
               f'fill="{C["rose"]}" opacity=".1"/>')
    out.append(note(40, 512, 'The brain is the exception, and that is exactly why the legal definition of death moved to it.', 14, C['ink']))
    return _svg(''.join(out), title='How long different organs remain viable after circulation stops')


def death_definitions():
    """Two definitions, and why the old one broke."""
    out = [label(40, 46, 'Why the definition had to change', 22),
           note(40, 68, 'For most of history death meant one thing. Then we learned to restart hearts.')]
    boxes = [
        (40, 120, C['muted'], 'The old definition', 'The heart has stopped',
         ['Worked for thousands of years.', 'Broke the moment CPR and',
          'defibrillators existed — people', 'came back.']),
        (500, 120, C['blue'], 'The definition now', 'The brain has stopped',
         ['The one part that cannot be', 'restarted, replaced or waited on.',
          'Everything else can be kept going', 'by a machine.']),
    ]
    for x, y, col, kicker, head, lines in boxes:
        out.append(panel(x, y, 400, 300, col, .08))
        out.append(tag(x + 26, y + 44, kicker, col))
        out.append(label(x + 26, y + 100, head, 20))
        for j, ln in enumerate(lines):
            out.append(note(x + 26, y + 140 + j * 24, ln, 14.5))
    out.append(arrow(452, 270, 488, 270, C['ink'], 3))
    out.append(note(40, 470, 'This is why "brain death" and "cardiac death" are different things, and why only one of them is final.', 14, C['ink']))
    return _svg(''.join(out), title='The old and current definitions of death, side by side')


# ================================================================ IMMUNE

def immune_layers():
    """Three lines of defence, drawn as layers."""
    out = [label(40, 46, 'Three lines of defence', 22),
           note(40, 68, 'Almost everything is stopped by the first one. You never find out about any of it.')]
    layers = [
        (C['teal'], 'Barrier', 'Skin, mucus, stomach acid, tears', 'Stops ~99% of everything, all the time'),
        (C['blue'], 'Innate', 'Cells that eat anything without the right password', 'Minutes. No memory, no targeting'),
        (C['violet'], 'Adaptive', 'Cells built to match this exact invader', 'Days. Remembers for decades'),
    ]
    y0 = 120
    for i, (col, name, what, speed) in enumerate(layers):
        y = y0 + i * 118
        out.append(f'<rect x="40" y="{y}" width="860" height="98" rx="18" fill="{col}" opacity=".1"/>')
        out.append(f'<rect x="40" y="{y}" width="12" height="98" rx="6" fill="{col}"/>')
        out.append(tag(76, y + 34, name, col))
        out.append(label(76, y + 74, what, 16))
        out.append(note(876, y + 40, speed, 13.5, col, 'end'))
    # invaders trying to get through
    for i, x in enumerate([250, 420, 590, 760]):
        out.append(cell(x, 100, 13, C['rose'], spikes=8))
    return _svg(''.join(out), title='The three layers of immune defence, from barrier to adaptive')


def immune_battle():
    """How a single infection goes, over days."""
    out = [label(40, 46, 'How one infection actually goes', 22),
           note(40, 68, 'You feel worst around day three — not when the invaders are winning, but when your own response peaks.')]
    x0, x1, y0, y1 = 90, 880, 150, 400
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{C["line"]}" stroke-width="2"/>')

    def curve(fn, col, dash=''):
        pts = []
        for i in range(101):
            t = i / 100
            pts.append((x0 + t * (x1 - x0), y1 - fn(t) * (y1 - y0)))
        d = 'M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts)
        return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" '
                f'stroke-linecap="round" {dash}/>')

    import math
    out.append(curve(lambda t: max(0, math.exp(-((t - .28) / .17) ** 2) * .92 - (t - .5) * .6 if t > .5 else math.exp(-((t - .28) / .17) ** 2) * .92), C['rose'], 'stroke-dasharray="8 6"'))
    out.append(curve(lambda t: min(1, .07 + (t ** 1.5) * 1.3), C['blue']))

    out.append(tag(x0 + 20, y0 - 14, 'invaders', C['rose']))
    out.append(tag(x0 + 150, y0 - 14, 'your defences', C['blue']))

    marks = [(.05, 'The cut'), (.28, 'You feel worst'), (.55, 'Specialists arrive'), (.92, 'Over')]
    for f, txt in marks:
        x = x0 + f * (x1 - x0)
        out.append(f'<line x1="{x:.0f}" y1="{y0 - 30}" x2="{x:.0f}" y2="{y1}" stroke="{C["line"]}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(note(x, y1 + 26, txt, 13.5, anchor='middle'))
    out.append(note(40, 500, 'The fever, the swelling and the aching are all your side of the fight.', 14, C['ink']))
    return _svg(''.join(out), title='Invader numbers against immune response over the days after an infection')


def immune_vaccine():
    """Why a vaccine works, in three steps."""
    steps = [
        (C['teal'], '1', 'A harmless piece', 'A vaccine shows your immune system part of an invader — never the working thing.'),
        (C['violet'], '2', 'The full rehearsal', 'Your body builds matching cells exactly as it would in a real infection, and you feel a bit rough for a day.'),
        (C['green'], '3', 'The memory stays', 'Meet the real one later and the fight is over before you notice it started.'),
    ]
    out = [label(40, 46, 'Why a vaccine works', 22),
           note(40, 68, 'It is not medicine you take when ill. It is a rehearsal, run in advance.')]
    for i, (col, n, head, body) in enumerate(steps):
        x = 40 + i * 300
        out.append(panel(x, 120, 270, 290, col, .1))
        out.append(f'<circle cx="{x + 48}" cy="{170}" r="26" fill="{col}"/>')
        out.append(label(x + 48, 178, n, 22, '#fff', 'middle', 800))
        out.append(label(x + 24, 236, head, 17))
        words, line, lines = body.split(), '', []
        for wd in words:
            if len(line + wd) > 28:
                lines.append(line); line = ''
            line += wd + ' '
        lines.append(line)
        for j, ln in enumerate(lines[:6]):
            out.append(note(x + 24, 268 + j * 21, ln.strip(), 13.5))
        if i < 2:
            out.append(arrow(x + 276, 265, x + 296, 265, C['muted'], 2.5))
    out.append(note(40, 470, 'The soreness afterwards is the rehearsal working. It is the same machinery, running without the danger.', 14, C['ink']))
    return _svg(''.join(out), title='The three steps by which a vaccine builds immunity')


# ================================================================ AGEING

def age_hallmarks():
    """What is actually going wrong inside a cell."""
    out = [label(40, 46, 'What ageing actually is', 22),
           note(40, 68, 'Not one process. Several specific ones, each of which is a thing you could in principle target.')]
    cx, cy, r = 250, 300, 150
    out.append(cell(cx, cy, r, C['blue'], nucleus=C['indigo']))
    out.append(note(cx, cy + 8, 'a cell', 15, '#fff', 'middle'))

    marks = [
        (-0.95, 'Caps wear down', C['pink'], 'DNA loses a little protection each division'),
        (-0.32, 'Errors build up', C['orange'], 'Damage accumulates faster than repair'),
        (0.32, 'Cells stop dividing', C['amber'], 'But refuse to leave, and leak inflammation'),
        (0.95, 'Power supply fails', C['violet'], 'Mitochondria produce less, and leak more'),
    ]
    import math
    for i, (ang, name, col, desc) in enumerate(marks):
        a = ang
        px, py = cx + math.cos(a) * (r + 6), cy + math.sin(a) * (r + 6)
        lx, ly = 560, 150 + i * 96
        out.append(leader(px, py, lx - 14, ly - 4, col))
        out.append(tag(lx, ly, name, col))
        out.append(note(lx, ly + 32, desc, 13.5))
    return _svg(''.join(out), title='A cell labelled with the main processes behind ageing')


def age_curves():
    """Damage against repair, and where they cross."""
    out = [label(40, 46, 'Why it starts mattering in mid-life', 22),
           note(40, 68, 'Nothing dramatic happens at any particular age. Two lines simply cross.')]
    x0, x1, y0, y1 = 90, 880, 140, 400
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{C["line"]}" stroke-width="2"/>')

    def curve(fn, col):
        pts = [(x0 + (i / 100) * (x1 - x0), y1 - fn(i / 100) * (y1 - y0)) for i in range(101)]
        return ('<path d="M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts) +
                f'" fill="none" stroke="{col}" stroke-width="4.5" stroke-linecap="round"/>')

    dmg = lambda t: min(1, (t ** 1.9) * 1.35)
    rep = lambda t: max(.05, 1 - (t ** 1.6) * 1.15)
    out.append(curve(dmg, C['rose']))
    out.append(curve(rep, C['green']))

    # find the crossing
    cross = 0
    for i in range(101):
        if dmg(i / 100) >= rep(i / 100):
            cross = i / 100
            break
    cxp = x0 + cross * (x1 - x0)
    out.append(f'<line x1="{cxp:.0f}" y1="{y0 - 20}" x2="{cxp:.0f}" y2="{y1}" stroke="{C["violet"]}" '
               f'stroke-width="2" stroke-dasharray="6 5"/>')
    out.append(f'<circle cx="{cxp:.0f}" cy="{y1 - dmg(cross) * (y1 - y0):.0f}" r="9" fill="{C["violet"]}"/>')
    out.append(tag(cxp - 60, y0 - 30, 'the lines cross', C['violet']))

    out.append(tag(x0 + 20, y0 + 6, 'damage', C['rose']))
    out.append(tag(x0 + 20, y0 + 44, 'ability to repair', C['green']))
    for f, t in [(0, 'birth'), (.5, '50'), (1, '100')]:
        out.append(note(x0 + f * (x1 - x0), y1 + 28, t, 13.5, anchor='middle'))
    out.append(note(40, 500, 'Before the crossing you are being rebuilt faster than you are wearing out. After it, you are not.', 14, C['ink']))
    return _svg(''.join(out), title='Damage and repair curves across a human lifespan, and where they cross')


def age_levers():
    """What actually moves the needle, ranked honestly."""
    rows = [
        ('Not smoking', .96, C['green'], 'Largest single effect anyone has measured'),
        ('Physical activity', .82, C['lime'], 'Strongest evidence of anything you can start today'),
        ('Sleep', .7, C['teal'], 'Consistent short sleep tracks with almost every age-related disease'),
        ('Diet quality', .62, C['cyan'], 'Real but smaller than usually claimed'),
        ('Social connection', .58, C['blue'], 'Comparable to well-known physical risks'),
        ('Supplements', .12, C['muted'], 'Almost nothing survives a proper trial'),
    ]
    out = [label(40, 46, 'What actually slows it down', 22),
           note(40, 68, 'Ranked by strength of evidence, not by how much attention each one gets.')]
    x0, w = 260, 640
    for i, (name, frac, col, desc) in enumerate(rows):
        y = 112 + i * 68
        out.append(label(40, y + 20, name, 15.5))
        out.append(bar(x0, y, w, 26, frac, col))
        out.append(note(x0, y + 46, desc, 12.5, col))
    out.append(note(40, 544, 'The boring ones win. That has been the consistent finding for decades, and nothing has displaced it.', 14, C['ink']))
    return _svg(''.join(out), title='Interventions that affect healthy lifespan, ranked by evidence')


# ---------------------------------------------------------------- thumbs

def _thumb(body, title):
    return _svg(body, w=600, h=400, title=title)


def thumb_sleep():
    out = [f'<rect width="600" height="400" rx="0" fill="{C["indigo"]}" opacity=".06"/>']
    rows = [C['amber'], C['pink'], C['cyan'], C['indigo']]
    for i, col in enumerate(rows):
        out.append(f'<rect x="60" y="{80 + i * 66}" width="480" height="52" rx="10" fill="{col}" opacity=".14"/>')
    pts = [(0, 0), (.08, 2), (.2, 3), (.3, 1), (.42, 3), (.54, 1), (.64, 2), (.76, 1), (.88, 2), (1, 0)]
    d = 'M' + ' L'.join(f'{60 + f * 480:.0f} {80 + st * 66 + 26:.0f}' for f, st in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{C["ink"]}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
    out.append(label(60, 52, 'A NIGHT OF SLEEP', 17, C['muted']))
    return _thumb(''.join(out), 'A hypnogram showing sleep cycles through the night')


def thumb_death():
    out = [f'<rect width="600" height="400" rx="0" fill="{C["rose"]}" opacity=".05"/>']
    out.append(label(60, 52, 'WHAT STOPS, AND WHEN', 17, C['muted']))
    organs = [('Brain', .04, C['rose']), ('Heart', .3, C['red']), ('Liver', .55, C['amber']), ('Cornea', 1.0, C['teal'])]
    for i, (n, f, col) in enumerate(organs):
        y = 110 + i * 66
        out.append(note(60, y + 22, n, 15, C['ink']))
        out.append(bar(180, y, 360, 30, f, col))
    return _thumb(''.join(out), 'Bars showing how long different organs stay viable')


def thumb_immune():
    out = [f'<rect width="600" height="400" rx="0" fill="{C["blue"]}" opacity=".05"/>']
    out.append(label(60, 52, 'THREE LINES OF DEFENCE', 17, C['muted']))
    for i, (col, n) in enumerate([(C['teal'], 'BARRIER'), (C['blue'], 'INNATE'), (C['violet'], 'ADAPTIVE')]):
        y = 100 + i * 92
        out.append(f'<rect x="60" y="{y}" width="480" height="74" rx="14" fill="{col}" opacity=".14"/>')
        out.append(f'<rect x="60" y="{y}" width="10" height="74" rx="5" fill="{col}"/>')
        out.append(label(88, y + 44, n, 16, col))
    for x in [200, 300, 400, 490]:
        out.append(cell(x, 82, 12, C['rose'], spikes=8))
    return _thumb(''.join(out), 'Three stacked layers of immune defence with invaders above')


def thumb_age():
    out = [f'<rect width="600" height="400" rx="0" fill="{C["violet"]}" opacity=".05"/>']
    out.append(label(60, 52, 'DAMAGE VS REPAIR', 17, C['muted']))
    x0, x1, y0, y1 = 70, 540, 100, 330
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{C["line"]}" stroke-width="2"/>')
    for fn, col in [(lambda t: min(1, (t ** 1.9) * 1.35), C['rose']),
                    (lambda t: max(.05, 1 - (t ** 1.6) * 1.15), C['green'])]:
        pts = [(x0 + (i / 60) * (x1 - x0), y1 - fn(i / 60) * (y1 - y0)) for i in range(61)]
        out.append('<path d="M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts) +
                   f'" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    out.append(f'<circle cx="{x0 + .52 * (x1 - x0):.0f}" cy="205" r="11" fill="{C["violet"]}"/>')
    return _thumb(''.join(out), 'Two crossing curves showing damage overtaking repair')


DIAGRAMS = {
    'sleep_architecture': sleep_architecture,
    'sleep_jobs': sleep_jobs,
    'sleep_debt': sleep_debt,
    'death_sequence': death_sequence,
    'death_viability': death_viability,
    'death_definitions': death_definitions,
    'immune_layers': immune_layers,
    'immune_battle': immune_battle,
    'immune_vaccine': immune_vaccine,
    'age_hallmarks': age_hallmarks,
    'age_curves': age_curves,
    'age_levers': age_levers,
}

THUMBS = {
    'sleep': thumb_sleep,
    'death': thumb_death,
    'immune': thumb_immune,
    'age': thumb_age,
}


def render(name):
    return DIAGRAMS[name]()


def thumb(name):
    return THUMBS[name]()


# ==================================================================
# PARAMETERISED DIAGRAM GRAMMAR
#
# The twelve diagrams above are hand-composed one-offs for the four
# flagship stories. That does not scale to fifty.
#
# These seven types take their content as data — every title, label,
# number and colour comes from the story. The visual language is shared
# (that is the point: a reader learns to read one and can read them all)
# while the content is entirely per-story. Same principle as any
# infographic desk: a chart vocabulary, bespoke content inside it.
# ==================================================================

SEQ = ['blue', 'rose', 'amber', 'green', 'violet', 'cyan', 'orange', 'teal', 'pink', 'indigo']


def _col(i):
    return C[SEQ[i % len(SEQ)]]


def _wrap(text, width):
    words, line, lines = text.split(), '', []
    for w in words:
        if len(line) + len(w) > width:
            lines.append(line.rstrip())
            line = ''
        line += w + ' '
    if line.strip():
        lines.append(line.rstrip())
    return lines


def _head(title, sub):
    out = [label(40, 46, title, 22)]
    if sub:
        for i, ln in enumerate(_wrap(sub, 96)[:2]):
            out.append(note(40, 70 + i * 20, ln, 13.5))
    return out


def d_timeline(title, sub, events, footer=''):
    """Ordered events on a line. events: [(frac, name, note)]"""
    out = _head(title, sub)
    x0, x1, y = 70, 880, 250
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{C["line"]}" '
               f'stroke-width="4" stroke-linecap="round"/>')
    for i, (f, name, desc) in enumerate(events):
        x = x0 + f * (x1 - x0)
        up = i % 2 == 0
        ty = y - 44 if up else y + 48
        col = _col(i)
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="19" fill="{col}" opacity=".2"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="10" fill="{col}"/>')
        out.append(f'<line x1="{x:.0f}" y1="{y + (-19 if up else 19)}" x2="{x:.0f}" '
                   f'y2="{ty + (14 if up else -14)}" stroke="{col}" stroke-width="2"/>')
        # Labels at the ends of the line would run past the viewBox if they
        # stayed centred on their dot, so the outer ones anchor inward instead.
        if x > VB_W - 160:
            anc, tx = 'end', VB_W - 24
        elif x < 160:
            anc, tx = 'start', 24
        else:
            anc, tx = 'middle', x
        out.append(label(tx, ty, name, 15, col, anc))
        for j, ln in enumerate(_wrap(desc, 24)[:2]):
            oy = ty - 42 + j * 18 if up else ty + 24 + j * 18
            out.append(note(tx, oy, ln, 12.5, anchor=anc))
    if footer:
        out.append(note(x0, 500, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_ranked(title, sub, rows, footer=''):
    """Bars, ranked. rows: [(label, 0..1, note)]"""
    out = _head(title, sub)
    x0, w = 270, 470
    top = 120
    for i, (name, frac, desc) in enumerate(rows):
        y = top + i * (330 // max(len(rows), 1) + 22)
        col = _col(i)
        out.append(label(40, y + 20, name, 15))
        out.append(bar(x0, y, w, 27, max(0.02, min(1, frac)), col))
        if desc:
            out.append(note(x0 + w + 16, y + 19, desc[:26], 12.5, col))
    if footer:
        out.append(note(40, 520, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_curves(title, sub, series, marks=(), footer='', axis=('', '')):
    """Two or more lines. series: [(name, [(0..1, 0..1)...])]"""
    out = _head(title, sub)
    x0, x1, y0, y1 = 90, 880, 150, 400
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{C["line"]}" stroke-width="2"/>')
    for i, (name, pts) in enumerate(series):
        col = _col(i)
        d = 'M' + ' L'.join(f'{x0 + px * (x1 - x0):.0f} {y1 - py * (y1 - y0):.0f}' for px, py in pts)
        dash = ' stroke-dasharray="8 6"' if i else ''
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" '
                   f'stroke-linecap="round"{dash}/>')
        out.append(tag(x0 + 16 + i * 168, y0 - 16, name, col))
    for f, txt in marks:
        x = x0 + f * (x1 - x0)
        out.append(f'<line x1="{x:.0f}" y1="{y0 - 4}" x2="{x:.0f}" y2="{y1}" '
                   f'stroke="{C["line"]}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(note(x, y1 + 26, txt, 13, anchor='middle'))
    if axis[0]:
        out.append(note(x0, y1 + 50, axis[0], 13))
    if axis[1]:
        out.append(note(x1, y1 + 50, axis[1], 13, anchor='end'))
    if footer:
        out.append(note(40, 520, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_layers(title, sub, rows, footer=''):
    """Stacked bands. rows: [(name, what, meta)]"""
    out = _head(title, sub)
    top = 120
    h = min(104, (400 - 0) // max(len(rows), 1))
    for i, (name, what, meta) in enumerate(rows):
        y = top + i * (h + 16)
        col = _col(i)
        out.append(f'<rect x="40" y="{y}" width="860" height="{h}" rx="18" fill="{col}" opacity=".1"/>')
        out.append(f'<rect x="40" y="{y}" width="12" height="{h}" rx="6" fill="{col}"/>')
        out.append(tag(78, y + 32, name, col))
        out.append(label(78, y + 70, what, 16))
        if meta:
            out.append(note(876, y + 38, meta, 13, col, 'end'))
    if footer:
        out.append(note(40, 530, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_compare(title, sub, left, right, footer=''):
    """Two panels. left/right: (kicker, head, [lines])"""
    out = _head(title, sub)
    for k, (side, x) in enumerate(((left, 40), (right, 500))):
        kicker, head, lines = side
        col = _col(k * 4)
        out.append(panel(x, 130, 400, 290, col, .08))
        out.append(tag(x + 26, 174, kicker, col))
        out.append(label(x + 26, 226, head, 19))
        for j, ln in enumerate(lines[:5]):
            out.append(note(x + 26, 262 + j * 24, ln, 14))
    out.append(arrow(452, 275, 488, 275, C['ink'], 3))
    if footer:
        out.append(note(40, 480, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_parts(title, sub, centre, callouts, footer=''):
    """A labelled thing with leader lines. callouts: [(name, note)]

    Anchors run top to bottom in the same order as the labels, because
    crossed leaders read as a mistake.
    """
    import math
    out = _head(title, sub)
    cx, cy, r = 250, 300, 145
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{_col(0)}" opacity=".18"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{_col(0)}" stroke-width="4"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*.45:.0f}" fill="{_col(0)}" opacity=".5"/>')
    for j, ln in enumerate(_wrap(centre, 14)[:2]):
        out.append(label(cx, cy + 6 + j * 20, ln, 15, '#fff', 'middle'))
    n = max(len(callouts), 1)
    for i, (name, desc) in enumerate(callouts):
        ang = -0.95 + (1.9 * i / max(n - 1, 1))
        px, py = cx + math.cos(ang) * (r + 6), cy + math.sin(ang) * (r + 6)
        lx, ly = 570, 150 + i * (300 // n if n > 1 else 1)
        col = _col(i + 1)
        out.append(leader(px, py, lx - 14, ly - 4, col))
        out.append(tag(lx, ly, name, col))
        for j, line in enumerate(_wrap(desc, 32)[:2]):
            out.append(note(lx, ly + 30 + j * 18, line, 13))
    if footer:
        out.append(note(40, 530, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


def d_field(title, sub, share, lit_label, dim_label, footer=''):
    """A grid of dots showing a proportion, with both parts named."""
    out = _head(title, sub)
    cols, rows = 24, 8
    total = cols * rows
    lit = round(total * max(0, min(1, share)))
    for i in range(total):
        x = 60 + (i % cols) * 34
        y = 130 + (i // cols) * 34
        if i < lit:
            out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{_col(0)}"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{C["shade"]}" '
                       f'stroke="{C["line"]}" stroke-width="1.5"/>')
    out.append(f'<circle cx="72" cy="442" r="10" fill="{_col(0)}"/>')
    out.append(note(92, 448, lit_label + ' \u2014 ' + format(share * 100, '.0f') + '%', 14, C['ink']))
    out.append(f'<circle cx="72" cy="482" r="8" fill="{C["shade"]}" stroke="{C["line"]}" stroke-width="1.5"/>')
    out.append(note(92, 488, dim_label + ' \u2014 ' + format((1 - share) * 100, '.0f') + '%', 14, C['muted']))
    if footer:
        out.append(note(40, 534, footer, 14, C['ink']))
    return _svg(''.join(out), title=title)


KINDS = {
    'timeline': d_timeline,
    'ranked': d_ranked,
    'curves': d_curves,
    'layers': d_layers,
    'compare': d_compare,
    'parts': d_parts,
    'field': d_field,
}


def build(spec):
    """spec: {'kind': ..., plus that kind's arguments}"""
    s = dict(spec)
    kind = s.pop('kind')
    return KINDS[kind](**s)
