# -*- coding: utf-8 -*-
"""Fold site/ into one self-contained HTML file.

The deployed site is the real artefact. This exists so the whole thing can be
opened, reviewed or sent to someone without a server, a build step or a network
connection: fonts, CSS and JS are inlined, every page body is carried as data,
and navigation is rewritten to swap pages in place.

    python3 bundle.py            -> context-site.html
"""
import base64
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(ROOT, 'context-site.html')
OUT_FRAGMENT = os.path.join(ROOT, 'context-artifact.html')


def read(*p):
    with open(os.path.join(SITE, *p), encoding='utf-8') as fh:
        return fh.read()


def data_uri(path):
    with open(path, 'rb') as fh:
        return 'data:font/woff2;base64,' + base64.b64encode(fh.read()).decode()


def collect():
    """Every page, keyed by the path links already use."""
    pages = {}
    for dirpath, _, names in os.walk(SITE):
        for n in sorted(names):
            if not n.endswith('.html'):
                continue
            full = os.path.join(dirpath, n)
            key = os.path.relpath(full, SITE).replace(os.sep, '/')
            pages[key] = open(full, encoding='utf-8').read()
    return pages


def body_of(html):
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.S)
    return m.group(1) if m else html


def title_of(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return m.group(1).strip() if m else ''


def theme_of(html):
    m = re.search(r'<body[^>]*class="([^"]*)"', html)
    return m.group(1) if m else ''


def main():
    css = read('assets', 'style.css')
    for name, file in (('gabarito.woff2', 'gabarito.woff2'),
                       ('source-sans-3.woff2', 'source-sans-3.woff2')):
        css = css.replace(f"url('fonts/{name}')",
                          f"url('{data_uri(os.path.join(SITE, 'assets', 'fonts', file))}')")
    js = read('assets', 'motion.js')

    pages = {}
    for key, html in collect().items():
        pages[key] = {'t': title_of(html), 'c': theme_of(html), 'b': body_of(html)}

    # A page body may contain </script>, which would close the block it is
    # embedded in. Escaping the slash keeps the JSON valid and the string intact.
    blob = json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')

    js_blob = json.dumps(js).replace('</', '<\\/')

    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[Context] &#8212; the whole site, in one file</title>
<style>{css}
html, body {{ margin: 0; }}
#bundle-frame {{ display: block; width: 100%; height: 100vh; border: 0; }}
</style>
</head>
<body>
<iframe id="bundle-frame" title="[Context]"></iframe>
<script>
var PAGES = {blob};
var CSS = document.querySelector('style').textContent;
var JS = {js_blob};
var frame = document.getElementById('bundle-frame');

function shell(key) {{
  var p = PAGES[key] || PAGES['index.html'];
  return '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1">'
    + '<title>' + p.t + '</title><style>' + CSS + '</style></head>'
    + '<body class="' + p.c + '">' + p.b
    + '<scr' + 'ipt>' + JS + '</scr' + 'ipt></body></html>';
}}

function resolve(from, href) {{
  // Links are relative to the page they sit on, so '../stories.html' from
  // 'papers/x.html' has to resolve the same way a real server would.
  var base = from.indexOf('/') > -1 ? from.slice(0, from.lastIndexOf('/') + 1) : '';
  var parts = (base + href).split('/');
  var out = [];
  for (var i = 0; i < parts.length; i++) {{
    if (parts[i] === '..') out.pop();
    else if (parts[i] && parts[i] !== '.') out.push(parts[i]);
  }}
  return out.join('/');
}}

var current = 'index.html';

function show(key) {{
  current = key;
  frame.srcdoc = shell(key);
  if (location.hash.slice(1) !== key) history.replaceState(null, '', '#' + key);
}}

frame.addEventListener('load', function () {{
  var d = frame.contentDocument;
  if (!d) return;
  d.addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || /^(https?:|mailto:|#)/.test(href)) return;
    var key = resolve(current, href);
    if (PAGES[key]) {{ e.preventDefault(); show(key); frame.contentWindow.scrollTo(0, 0); }}
  }});
}});

window.addEventListener('hashchange', function () {{
  var k = location.hash.slice(1);
  if (PAGES[k] && k !== current) show(k);
}});

show(PAGES[location.hash.slice(1)] ? location.hash.slice(1) : 'index.html');
</script>
</body>
</html>
'''
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(doc)
    print(f'{len(pages)} pages -> {OUT} ({os.path.getsize(OUT) / 1e6:.1f} MB)')

    # A hosted-artifact copy: same payload, no outer document, because the host
    # supplies the doctype and head. The wrapper stays invisible on purpose —
    # [Context] already has a design system and the frame should not comment on
    # it. The site commits to one visual world (white page, dark panels) by the
    # rule in STYLE.md, so the shell holds that ground in either viewer theme
    # rather than inverting into a mismatched band around the page.
    body = doc[doc.index('<body>') + len('<body>'):doc.rindex('</body>')]
    frag = ('<style>\n' + css
            + '\n:root, :root[data-theme="dark"], :root[data-theme="light"] {'
              ' color-scheme: light; background: #FFFFFF; }\n'
              'html, body { margin: 0; background: #FFFFFF; }\n'
              '#bundle-frame { display: block; width: 100%; height: 100vh;'
              ' border: 0; background: #FFFFFF; }\n</style>\n'
            + body.strip() + '\n')
    with open(OUT_FRAGMENT, 'w', encoding='utf-8') as fh:
        fh.write(frag)
    print(f'{len(pages)} pages -> {OUT_FRAGMENT} '
          f'({os.path.getsize(OUT_FRAGMENT) / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
