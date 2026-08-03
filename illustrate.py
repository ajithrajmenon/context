# -*- coding: utf-8 -*-
"""Rich vector illustration, generated.

The old scenes were particle systems — dots and lines over a gradient. That
reads as decoration no matter how many hues you give it. Illustration is
different: dozens of designed forms, layered front to back, filling the
frame, each carrying its own colour.

So these are composed rather than simulated. Every scene returns SVG made of
real shapes — membranes, organelles, planets, figures, buildings, neurons —
built from a deterministic seed so a page looks the same on every load.

Depth is the thing that stops it looking flat: each scene lays down a soft
background wash, then midground forms at partial opacity, then crisp
foreground with outlines and interior detail. Motion is CSS on groups, so
the browser can hand the whole thing to the compositor.
"""
import math
import random

# The house palette. Bright enough to sit on a deep ground, saturated enough
# to hold their own next to each other.
P = {
    'cyan':    '#22D3EE',
    'lime':    '#A3E635',
    'magenta': '#F472B6',
    'violet':  '#A78BFA',
    'amber':   '#FBBF24',
    'emerald': '#34D399',
    'coral':   '#FB7185',
    'sky':     '#60A5FA',
    'orchid':  '#C084FC',
    'teal':    '#2DD4BF',
    'gold':    '#FCD34D',
    'rose':    '#FDA4AF',
    'mint':    '#6EE7B7',
    'indigo':  '#818CF8',
}
SPREAD = [P['cyan'], P['lime'], P['magenta'], P['violet'], P['amber'],
          P['emerald'], P['coral'], P['sky'], P['orchid'], P['teal'],
          P['gold'], P['mint'], P['indigo'], P['rose']]

W, H = 1200, 700


def _r(seed):
    return random.Random(seed)


def _anim(kind, dur, delay=0.0):
    return f'class="il-{kind}" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"'


# ---------------------------------------------------------------- pieces

def blob(rr, cx, cy, r, col, op=1.0, detail=0):
    """An organic lump. Randomised radii so nothing looks machine-made."""
    pts, n = [], 9
    for i in range(n):
        a = (i / n) * math.tau
        rad = r * (0.82 + rr.random() * 0.36)
        pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
    d = f'M{pts[0][0]:.0f} {pts[0][1]:.0f}'
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d += f' Q{x0:.0f} {y0:.0f} {mx:.0f} {my:.0f}'
    d += ' Z'
    out = f'<path d="{d}" fill="{col}" opacity="{op}"/>'
    for _ in range(detail):
        a = rr.random() * math.tau
        rad = rr.random() * r * 0.55
        out += (f'<circle cx="{cx + math.cos(a) * rad:.0f}" cy="{cy + math.sin(a) * rad:.0f}" '
                f'r="{2 + rr.random() * 4:.0f}" fill="#fff" opacity="{0.25 + rr.random() * 0.3:.2f}"/>')
    return out


def wash(rr, n=7):
    """Soft out-of-focus colour behind everything, for depth."""
    out = []
    for i in range(n):
        cx, cy = rr.uniform(0, W), rr.uniform(0, H)
        r = rr.uniform(150, 340)
        col = SPREAD[rr.randrange(len(SPREAD))]
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{col}" opacity="0.10"/>')
    return ''.join(out)


def motes(rr, n=46):
    """Small drifting flecks — the confetti that fills negative space."""
    out = []
    for i in range(n):
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        r = rr.uniform(2, 7)
        col = SPREAD[rr.randrange(len(SPREAD))]
        out.append(f'<circle {_anim("float", rr.uniform(5, 11), rr.uniform(0, 5))} '
                   f'cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{col}" opacity="{rr.uniform(.35, .85):.2f}"/>')
    return ''.join(out)


def figure(x, y, s, col, rr):
    """A stylised person: head and a rounded body. Deliberately simple."""
    return (f'<g {_anim("bob", rr.uniform(3.5, 7), rr.uniform(0, 4))}>'
            f'<circle cx="{x:.0f}" cy="{y - s * 1.5:.0f}" r="{s * .62:.1f}" fill="{col}"/>'
            f'<path d="M{x - s * .78:.0f} {y + s * 1.5:.0f} '
            f'a{s * .78:.0f} {s * 1.7:.0f} 0 0 1 {s * 1.56:.0f} 0 Z" fill="{col}"/>'
            f'</g>')


def organelle(rr, cx, cy, r, col):
    """Something living inside a cell — a lump with an outline and a core."""
    return (f'<g {_anim("drift", rr.uniform(7, 14), rr.uniform(0, 6))}>'
            + blob(rr, cx, cy, r, col, 0.9)
            + f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * .34:.0f}" fill="#fff" opacity=".55"/>'
            + '</g>')


def virion(rr, cx, cy, r, col):
    """A virus: a capsid with spikes."""
    spikes = ''
    n = 11
    for i in range(n):
        a = (i / n) * math.tau
        spikes += (f'<line x1="{cx + math.cos(a) * r:.0f}" y1="{cy + math.sin(a) * r:.0f}" '
                   f'x2="{cx + math.cos(a) * r * 1.5:.0f}" y2="{cy + math.sin(a) * r * 1.5:.0f}" '
                   f'stroke="{col}" stroke-width="{r * .17:.1f}" stroke-linecap="round"/>')
        spikes += (f'<circle cx="{cx + math.cos(a) * r * 1.62:.0f}" cy="{cy + math.sin(a) * r * 1.62:.0f}" '
                   f'r="{r * .17:.1f}" fill="{col}"/>')
    return (f'<g {_anim("spin", rr.uniform(24, 46), rr.uniform(0, 8))} '
            f'style="transform-origin:{cx:.0f}px {cy:.0f}px;animation-duration:{rr.uniform(24, 46):.0f}s">'
            f'{spikes}<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{col}"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * .45:.0f}" fill="#0B1220" opacity=".45"/></g>')


def planet(rr, cx, cy, r, col, ringed=False):
    detail = ''
    for _ in range(rr.randrange(2, 5)):
        a = rr.random() * math.tau
        d = rr.uniform(0, r * .55)
        detail += (f'<circle cx="{cx + math.cos(a) * d:.0f}" cy="{cy + math.sin(a) * d:.0f}" '
                   f'r="{r * rr.uniform(.14, .3):.0f}" fill="#fff" opacity=".22"/>')
    rings = ''
    if ringed:
        rings = (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r * 1.75:.0f}" ry="{r * .42:.0f}" '
                 f'fill="none" stroke="{P["gold"]}" stroke-width="{r * .13:.1f}" opacity=".8"/>')
    return (f'<g {_anim("bob", rr.uniform(6, 12), rr.uniform(0, 5))}>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 1.5:.0f}" fill="{col}" opacity=".14"/>'
            f'{rings}<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{col}"/>{detail}</g>')


def star_burst(rr, cx, cy, r, col):
    pts = ''
    for i in range(4):
        a = (i / 4) * math.pi
        pts += (f'<line x1="{cx - math.cos(a) * r * 2:.0f}" y1="{cy - math.sin(a) * r * 2:.0f}" '
                f'x2="{cx + math.cos(a) * r * 2:.0f}" y2="{cy + math.sin(a) * r * 2:.0f}" '
                f'stroke="{col}" stroke-width="{r * .3:.1f}" stroke-linecap="round" opacity=".55"/>')
    return (f'<g {_anim("twinkle", rr.uniform(2.5, 6), rr.uniform(0, 4))}>{pts}'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{col}"/></g>')


# ---------------------------------------------------------------- scenes

def sc_cell(rr):
    """Microbiology: big cells, organelles inside them, invaders around."""
    out = [wash(rr)]
    for i in range(4):                       # background cells, far back
        out.append(blob(rr, rr.uniform(0, W), rr.uniform(0, H), rr.uniform(120, 210),
                        SPREAD[rr.randrange(len(SPREAD))], .18))
    # the hero cell
    cx, cy, R = W * .58, H * .5, 210
    out.append(f'<g {_anim("breathe", 9)}>')
    out.append(blob(rr, cx, cy, R * 1.12, P['cyan'], .16))
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{P["teal"]}" opacity=".26"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{P["cyan"]}" stroke-width="7"/>')
    out.append('</g>')
    out.append(organelle(rr, cx - 30, cy - 20, 62, P['violet']))
    for i in range(11):                      # organelles
        a = rr.random() * math.tau
        d = rr.uniform(70, R * .82)
        out.append(organelle(rr, cx + math.cos(a) * d, cy + math.sin(a) * d,
                             rr.uniform(15, 34), SPREAD[i % len(SPREAD)]))
    for i in range(9):                       # invaders closing in
        a = rr.random() * math.tau
        d = rr.uniform(R * 1.25, R * 2.1)
        out.append(virion(rr, cx + math.cos(a) * d, cy + math.sin(a) * d * .8,
                          rr.uniform(13, 24), [P['magenta'], P['coral'], P['orchid']][i % 3]))
    for i in range(13):                      # free-floating bacteria
        out.append(blob(rr, rr.uniform(0, W), rr.uniform(0, H), rr.uniform(14, 34),
                        SPREAD[rr.randrange(len(SPREAD))], .85, detail=2))
    out.append(motes(rr, 40))
    return ''.join(out)


def sc_cosmos(rr):
    """Planets, stars and nebulae, all different."""
    out = [wash(rr, 8)]
    for i in range(30):
        out.append(star_burst(rr, rr.uniform(0, W), rr.uniform(0, H), rr.uniform(2.5, 7),
                              [P['gold'], P['sky'], P['cyan'], P['rose'], '#fff'][i % 5]))
    out.append(planet(rr, W * .22, H * .62, 118, P['indigo']))
    out.append(planet(rr, W * .72, H * .3, 74, P['coral'], ringed=True))
    out.append(planet(rr, W * .86, H * .72, 44, P['emerald']))
    out.append(planet(rr, W * .46, H * .2, 30, P['amber']))
    out.append(planet(rr, W * .56, H * .8, 52, P['orchid']))
    # a comet
    out.append(f'<g {_anim("drift", 16)}><path d="M{W*.34:.0f} {H*.36:.0f} l 150 -54" '
               f'stroke="{P["cyan"]}" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
               f'<circle cx="{W*.34:.0f}" cy="{H*.36:.0f}" r="11" fill="{P["cyan"]}"/></g>')
    out.append(motes(rr, 34))
    return ''.join(out)


def sc_crowd(rr):
    """Rows of people. Most of them dim: everyone who came before."""
    out = [wash(rr, 5)]
    rows, per = 7, 20
    for r_ in range(rows):
        for i in range(per):
            x = 34 + i * (W - 68) / (per - 1) + (r_ % 2) * 14
            y = 120 + r_ * (H - 180) / (rows - 1)
            base = 20 - r_ * 0.7
            alive = ((r_ * per + i) % 15) == 0
            if alive:
                # the living: bigger, saturated, with a halo so they carry
                col = SPREAD[(r_ * 3 + i) % len(SPREAD)]
                out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{base * 2.6:.0f}" '
                           f'fill="{col}" opacity=".2"/>')
                out.append(figure(x, y, base * 1.35, col, rr))
            else:
                col = SPREAD[(r_ * 5 + i * 3) % len(SPREAD)]
                out.append(f'<g opacity=".3">{figure(x, y, base, col, rr)}</g>')
    out.append(motes(rr, 26))
    return ''.join(out)


def sc_city(rr):
    """A skyline with plants taking it back."""
    out = [wash(rr, 6)]
    x = -20
    while x < W:
        bw = rr.uniform(58, 118)
        bh = rr.uniform(150, 420)
        col = [P['indigo'], P['sky'], P['violet']][rr.randrange(3)]
        out.append(f'<rect x="{x:.0f}" y="{H - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" '
                   f'rx="10" fill="{col}" opacity=".5"/>')
        for wy in range(int(bh // 44)):      # lit windows
            for wx in range(int(bw // 34)):
                if rr.random() < .5:
                    continue
                out.append(f'<rect x="{x + 12 + wx * 34:.0f}" y="{H - bh + 20 + wy * 44:.0f}" '
                           f'width="14" height="18" rx="3" '
                           f'fill="{[P["gold"], P["amber"], P["cyan"]][rr.randrange(3)]}" '
                           f'opacity="{rr.uniform(.4, .95):.2f}"/>')
        x += bw + rr.uniform(12, 30)
    # vines climbing over the lot
    for i in range(26):
        vx = rr.uniform(0, W)
        vh = rr.uniform(120, 400)
        col = [P['lime'], P['emerald'], P['mint']][rr.randrange(3)]
        d = f'M{vx:.0f} {H}'
        for s in range(1, 7):
            d += f' q {rr.uniform(-34, 34):.0f} {-vh / 6:.0f} {rr.uniform(-16, 16):.0f} {-vh / 6:.0f}'
        out.append(f'<g {_anim("sway", rr.uniform(6, 12), rr.uniform(0, 4))}>'
                   f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" '
                   f'stroke-linecap="round" opacity=".9"/>'
                   f'<circle cx="{vx:.0f}" cy="{H - vh:.0f}" r="9" '
                   f'fill="{[P["magenta"], P["gold"], P["coral"]][rr.randrange(3)]}"/></g>')
    out.append(motes(rr, 22))
    return ''.join(out)


def sc_ocean(rr):
    """Zones of sea, dark shapes near the light, glowing life below it."""
    out = []
    bands = [(0, .2, P['cyan']), (.2, .44, P['teal']), (.44, .7, P['sky']), (.7, 1, P['indigo'])]
    for a, b, col in bands:
        out.append(f'<rect x="0" y="{a * H:.0f}" width="{W}" height="{(b - a) * H:.0f}" '
                   f'fill="{col}" opacity=".2"/>')
        out.append(f'<line x1="0" y1="{b * H:.0f}" x2="{W}" y2="{b * H:.0f}" '
                   f'stroke="{col}" stroke-width="2" opacity=".55"/>')
    # jellyfish, glowing, in the dark half
    for i in range(9):
        jx, jy = rr.uniform(60, W - 60), rr.uniform(H * .48, H * .95)
        r = rr.uniform(22, 48)
        col = [P['magenta'], P['orchid'], P['cyan'], P['lime']][i % 4]
        tent = ''
        for t in range(6):
            tx = jx - r * .7 + t * (r * 1.4 / 5)
            tent += (f'<path d="M{tx:.0f} {jy:.0f} q {rr.uniform(-12, 12):.0f} {r * .8:.0f} '
                     f'{rr.uniform(-10, 10):.0f} {r * 1.5:.0f}" fill="none" stroke="{col}" '
                     f'stroke-width="3" stroke-linecap="round" opacity=".75"/>')
        out.append(f'<g {_anim("bob", rr.uniform(5, 10), rr.uniform(0, 4))}>'
                   f'<circle cx="{jx:.0f}" cy="{jy:.0f}" r="{r * 1.9:.0f}" fill="{col}" opacity=".14"/>'
                   f'{tent}<path d="M{jx - r:.0f} {jy:.0f} a{r:.0f} {r * .82:.0f} 0 0 1 {r * 2:.0f} 0 Z" '
                   f'fill="{col}"/></g>')
    # silhouettes up in the light
    for i in range(11):
        fx, fy = rr.uniform(0, W), rr.uniform(20, H * .42)
        s = rr.uniform(10, 26)
        out.append(f'<g {_anim("drift", rr.uniform(9, 18), rr.uniform(0, 6))}>'
                   f'<path d="M{fx:.0f} {fy:.0f} q {s:.0f} {-s * .7:.0f} {s * 2:.0f} 0 '
                   f'q {-s:.0f} {s * .7:.0f} {-s * 2:.0f} 0 Z" fill="#0B1220" opacity=".55"/></g>')
    # vents on the floor
    for i in range(4):
        vx = rr.uniform(80, W - 80)
        out.append(f'<path d="M{vx - 34:.0f} {H} l 18 -60 l 32 0 l 18 60 Z" fill="#0B1220" opacity=".7"/>')
        for b in range(5):
            out.append(f'<circle {_anim("rise", rr.uniform(4, 8), rr.uniform(0, 4))} '
                       f'cx="{vx + rr.uniform(-12, 12):.0f}" cy="{H - 70 - b * 26:.0f}" '
                       f'r="{rr.uniform(4, 9):.0f}" fill="{P["amber"]}" opacity=".6"/>')
    out.append(motes(rr, 30))
    return ''.join(out)


def sc_mind(rr):
    """Neurons and the signals running between them."""
    out = [wash(rr, 6)]
    nodes = [(rr.uniform(90, W - 90), rr.uniform(80, H - 80)) for _ in range(15)]
    for i, (x, y) in enumerate(nodes):       # connections first, behind
        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]
            if math.hypot(x2 - x, y2 - y) > 320:
                continue
            out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                       f'stroke="{SPREAD[(i + j) % len(SPREAD)]}" stroke-width="2" opacity=".3"/>')
    for i, (x, y) in enumerate(nodes):
        col = SPREAD[i % len(SPREAD)]
        arms = ''
        for a in range(6):
            ang = (a / 6) * math.tau + rr.random()
            arms += (f'<line x1="{x:.0f}" y1="{y:.0f}" '
                     f'x2="{x + math.cos(ang) * 46:.0f}" y2="{y + math.sin(ang) * 46:.0f}" '
                     f'stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".8"/>')
        out.append(f'<g {_anim("pulse", rr.uniform(3, 7), rr.uniform(0, 4))}>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="46" fill="{col}" opacity=".14"/>'
                   f'{arms}<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="{col}"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#fff" opacity=".6"/></g>')
    out.append(motes(rr, 34))
    return ''.join(out)


def sc_colony(rr):
    """Ant nests, trails, leaves and the fungus they farm."""
    out = [wash(rr, 5)]
    nests = [(rr.uniform(110, W - 110), rr.uniform(110, H - 110)) for _ in range(6)]
    for i, (x, y) in enumerate(nests):
        for j in range(i + 1, len(nests)):
            x2, y2 = nests[j]
            out.append(f'<path d="M{x:.0f} {y:.0f} Q{(x + x2) / 2 + rr.uniform(-70, 70):.0f} '
                       f'{(y + y2) / 2 + rr.uniform(-70, 70):.0f} {x2:.0f} {y2:.0f}" '
                       f'fill="none" stroke="{P["amber"]}" stroke-width="2" opacity=".28"/>')
    for i in range(60):                      # the ants themselves
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        s = rr.uniform(4, 8)
        col = [P['amber'], P['gold'], P['coral']][rr.randrange(3)]
        out.append(f'<g {_anim("drift", rr.uniform(6, 13), rr.uniform(0, 6))}>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.1f}" fill="{col}"/>'
                   f'<circle cx="{x + s * 1.6:.0f}" cy="{y:.0f}" r="{s * .72:.1f}" fill="{col}"/>'
                   f'<circle cx="{x - s * 1.5:.0f}" cy="{y:.0f}" r="{s * .58:.1f}" fill="{col}"/></g>')
    for i, (x, y) in enumerate(nests):       # nests on top
        col = SPREAD[i * 2 % len(SPREAD)]
        out.append(f'<g {_anim("breathe", rr.uniform(5, 9), rr.uniform(0, 3))}>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="54" fill="{col}" opacity=".16"/>'
                   + blob(rr, x, y, 34, col, .95, detail=3) + '</g>')
    for i in range(12):                      # leaves being carried
        lx, ly = rr.uniform(0, W), rr.uniform(0, H)
        out.append(f'<g {_anim("sway", rr.uniform(5, 10), rr.uniform(0, 4))}>'
                   f'<path d="M{lx:.0f} {ly:.0f} q 22 -20 44 0 q -22 20 -44 0 Z" '
                   f'fill="{[P["lime"], P["emerald"], P["mint"]][i % 3]}" opacity=".9"/></g>')
    out.append(motes(rr, 26))
    return ''.join(out)


def sc_matter(rr):
    """Atoms, particle pairs and the empty space between them."""
    out = [wash(rr, 6)]
    for i in range(7):
        cx, cy = rr.uniform(120, W - 120), rr.uniform(110, H - 110)
        R = rr.uniform(58, 120)
        col = SPREAD[i % len(SPREAD)]
        shells = ''
        for s in range(3):
            rr_ = R * (.45 + s * .28)
            shells += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr_:.0f}" ry="{rr_ * .42:.0f}" '
                       f'fill="none" stroke="{col}" stroke-width="2.5" opacity=".5" '
                       f'transform="rotate({s * 60} {cx:.0f} {cy:.0f})"/>')
            for e in range(2):
                a = rr.random() * math.tau
                ex = cx + math.cos(a) * rr_
                ey = cy + math.sin(a) * rr_ * .42
                shells += (f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="6" '
                           f'fill="{SPREAD[(i + s + e) % len(SPREAD)]}"/>')
        out.append(f'<g {_anim("spin", rr.uniform(30, 60), rr.uniform(0, 8))} '
                   f'style="transform-origin:{cx:.0f}px {cy:.0f}px">{shells}</g>'
                   f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * .16:.0f}" fill="{P["magenta"]}"/>'
                   f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * .3:.0f}" fill="{P["magenta"]}" opacity=".2"/>')
    for i in range(16):                      # pairs blinking in and out
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        a, b = SPREAD[i % len(SPREAD)], SPREAD[(i + 5) % len(SPREAD)]
        out.append(f'<g {_anim("blink", rr.uniform(2.5, 6), rr.uniform(0, 5))}>'
                   f'<circle cx="{x - 14:.0f}" cy="{y:.0f}" r="7" fill="{a}"/>'
                   f'<circle cx="{x + 14:.0f}" cy="{y:.0f}" r="7" fill="{b}"/></g>')
    out.append(motes(rr, 30))
    return ''.join(out)


def sc_time(rr):
    """Order on the left, disorder on the right, and the drift between."""
    out = [wash(rr, 5)]
    cols, rows = 15, 8
    for r_ in range(rows):
        for c_ in range(cols):
            k = c_ / (cols - 1)
            jitter = k * k
            x = 60 + c_ * (W - 140) / (cols - 1) + rr.uniform(-60, 60) * jitter
            y = 70 + r_ * (H - 150) / (rows - 1) + rr.uniform(-60, 60) * jitter
            s = 26 - jitter * 10
            col = SPREAD[(r_ * 3 + c_) % len(SPREAD)]
            out.append(f'<rect {_anim("bob", rr.uniform(4, 9), rr.uniform(0, 5))} '
                       f'x="{x:.0f}" y="{y:.0f}" width="{s:.0f}" height="{s:.0f}" rx="7" '
                       f'fill="{col}" opacity="{1 - jitter * .35:.2f}" '
                       f'transform="rotate({rr.uniform(-40, 40) * jitter:.0f} {x + s / 2:.0f} {y + s / 2:.0f})"/>')
    out.append(motes(rr, 22))
    return ''.join(out)


def sc_sun(rr):
    """A star, its corona, and what it is doing to everything nearby."""
    out = [wash(rr, 6)]
    cx, cy = W * .34, H * .5
    for i in range(4):
        out.append(f'<circle {_anim("breathe", 6 + i * 1.5, i * .4)} cx="{cx:.0f}" cy="{cy:.0f}" '
                   f'r="{150 + i * 52}" fill="{[P["gold"], P["amber"], P["coral"], P["magenta"]][i]}" '
                   f'opacity="{.2 - i * .04:.2f}"/>')
    flares = ''
    for i in range(22):
        a = (i / 22) * math.tau
        L = 150 + rr.uniform(20, 90)
        flares += (f'<line x1="{cx + math.cos(a) * 140:.0f}" y1="{cy + math.sin(a) * 140:.0f}" '
                   f'x2="{cx + math.cos(a) * L:.0f}" y2="{cy + math.sin(a) * L:.0f}" '
                   f'stroke="{[P["gold"], P["amber"], P["coral"]][i % 3]}" stroke-width="7" '
                   f'stroke-linecap="round" opacity=".7"/>')
    out.append(f'<g {_anim("spin", 90)} style="transform-origin:{cx:.0f}px {cy:.0f}px">{flares}</g>')
    out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="140" fill="{P["gold"]}"/>')
    out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="140" fill="{P["amber"]}" opacity=".5"/>')
    out.append(planet(rr, W * .78, H * .34, 46, P['sky']))
    out.append(planet(rr, W * .88, H * .68, 30, P['emerald']))
    out.append(planet(rr, W * .64, H * .8, 22, P['coral']))
    for i in range(24):
        out.append(star_burst(rr, rr.uniform(W * .5, W), rr.uniform(0, H), rr.uniform(2, 6),
                              ['#fff', P['cyan'], P['gold']][i % 3]))
    out.append(motes(rr, 24))
    return ''.join(out)


SCENES = {
    'cell': sc_cell,
    'cosmos': sc_cosmos,
    'crowd': sc_crowd,
    'city': sc_city,
    'ocean': sc_ocean,
    'mind': sc_mind,
    'colony': sc_colony,
    'matter': sc_matter,
    'time': sc_time,
    'sun': sc_sun,
}


def render(name, seed, cls='art', light=False):
    """The full <svg> for a scene. Slice so it fills whatever box it is in.

    `light` trims the scene for card-sized panels: a card is a fraction of a
    hero's area, so the fine detail is invisible there and only costs bytes.
    Twenty full scenes on one index page is a third of a megabyte.
    """
    fn = SCENES.get(name, sc_cosmos)
    body = fn(_r(seed))
    if light:
        body = _thin(body)
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
            f'aria-hidden="true" focusable="false">{body}</svg>')


def _thin(body):
    """Drop every other small element. Keeps the composition, halves the bytes."""
    import re as _re
    parts = _re.findall(r'<(?:g|path|circle|rect|ellipse|line)\b.*?(?:</g>|/>)', body, _re.S)
    if not parts:
        return body
    keep, n = [], 0
    for part in parts:
        # always keep the big structural shapes, thin out the confetti
        small = ('r="' in part and _re.search(r'r="(\d+(?:\.\d+)?)"', part)
                 and float(_re.search(r'r="(\d+(?:\.\d+)?)"', part).group(1)) < 12)
        if small:
            n += 1
            if n % 2:
                continue
        keep.append(part)
    return ''.join(keep)
