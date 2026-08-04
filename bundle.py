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


def scripts_of(body):
    """Pull the page's own scripts out. innerHTML never runs them, so they are
    kept aside and re-executed deliberately after the body is swapped in."""
    code = re.findall(r'<script[^>]*>(.*?)</script>', body, re.S)
    return re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.S), code


def main():
    css = read('assets', 'style.css')
    for name in ('gabarito.woff2', 'source-sans-3.woff2'):
        css = css.replace(
            f"url('fonts/{name}')",
            f"url('{data_uri(os.path.join(SITE, 'assets', 'fonts', name))}')")
    js = read('assets', 'motion.js')

    pages = {}
    for key, html in collect().items():
        body, code = scripts_of(body_of(html))
        pages[key] = {'t': title_of(html), 'c': theme_of(html), 'b': body, 's': code}

    # A page body carries `</script>`, which would close the block it is
    # embedded in. Escaping the slash keeps the JSON valid and the text intact.
    blob = json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')
    start_key = 'index.html'

    runtime = """
var CTX = {
  nonce: (document.currentScript && document.currentScript.nonce) || '',
  root: document.getElementById('ctx-root'),
  current: ''
};

function ctxRun(code) {
  // A dynamically created script is blocked under a nonce policy unless it
  // carries the nonce, and eval is blocked outright. Stamping the nonce this
  // script was already served with is the one route that works in both a
  // strict host and a plain file:// open.
  var s = document.createElement('script');
  if (CTX.nonce) s.nonce = CTX.nonce;
  s.textContent = code;
  document.body.appendChild(s);
  s.remove();
}

function ctxResolve(from, href) {
  // Links are relative to the page holding them, so '../stories.html' from
  // 'papers/x.html' has to resolve the way a real server would.
  var base = from.indexOf('/') > -1 ? from.slice(0, from.lastIndexOf('/') + 1) : '';
  var parts = (base + href).split('/');
  var out = [];
  for (var i = 0; i < parts.length; i++) {
    if (parts[i] === '..') out.pop();
    else if (parts[i] && parts[i] !== '.') out.push(parts[i]);
  }
  return out.join('/');
}

function ctxShow(key, push) {
  var p = CTX_PAGES[key];
  if (!p) return;
  CTX.current = key;
  document.title = p.t;
  CTX.root.className = p.c;
  CTX.root.innerHTML = p.b;
  scrollTo(0, 0);
  for (var i = 0; i < p.s.length; i++) ctxRun(p.s[i]);
  if (window.contextInit) window.contextInit();
  if (push && location.hash.slice(1) !== key) {
    history.replaceState(null, '', '#' + key);
  }
}

document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var href = a.getAttribute('href');
  if (!href || /^(https?:|mailto:|#)/.test(href)) return;
  var key = ctxResolve(CTX.current, href);
  if (CTX_PAGES[key]) { e.preventDefault(); ctxShow(key, true); }
});

addEventListener('hashchange', function () {
  var k = location.hash.slice(1);
  if (CTX_PAGES[k] && k !== CTX.current) ctxShow(k, false);
});
"""

    # The site commits to one visual world by the rule in STYLE.md section 4 —
    # white page, dark panels — so the shell holds that ground in either viewer
    # theme rather than inverting into a mismatched band around the page.
    shell_css = (
        '\n:root, :root[data-theme="dark"], :root[data-theme="light"]'
        ' { color-scheme: light; }\n'
        'html, body { margin: 0; background: var(--page, #fff); }\n')

    parts = [
        '<style>', css, shell_css, '</style>\n',
        '<div id="ctx-root" class="', pages[start_key]['c'], '">',
        pages[start_key]['b'], '</div>\n',
        '<script>\n', js, '\n',
        'var CTX_PAGES = ', blob, ';\n',
        runtime,
        "ctxShow(CTX_PAGES[location.hash.slice(1)] ? location.hash.slice(1) : "
        + json.dumps(start_key) + ", false);\n",
        '</script>\n',
    ]
    frag = ''.join(parts)

    with open(OUT_FRAGMENT, 'w', encoding='utf-8') as fh:
        fh.write(frag)

    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<title>[Context] &#8212; the whole site, in one file</title>\n'
           '</head>\n<body>\n' + frag + '</body>\n</html>\n')
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(doc)

    for path in (OUT, OUT_FRAGMENT):
        print(f'{len(pages)} pages -> {path} ({os.path.getsize(path) / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
