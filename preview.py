# -*- coding: utf-8 -*-
"""Build the site and serve it, so you can look at it.

    python preview.py

Then open http://127.0.0.1:8000/. Stop it with Ctrl-C.

This is the public site on its own — no login, no database, no backoffice.
Change a story, run this again, reload.

Why a script rather than just opening site/index.html: pages link to each
other with paths like ../assets/style.css, and a browser opening a file:// URL
treats every page as its own origin. Some of it works, some of it silently
does not. A real HTTP server on localhost behaves the way GitHub Pages will,
which is the point of looking.

    python preview.py --port 9000     use a different port
    python preview.py --no-build      serve site/ as it stands, skip the build
"""
import functools
import http.server
import os
import socketserver
import subprocess
import sys
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')

for _stream in (sys.stdout, sys.stderr):
    try:
        # A Windows console is usually cp1252, which cannot encode the rule
        # below or an em-dash in a build message.
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError, OSError):
        pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # One line per page is noise; a failure is not.
        if not str(args[1] if len(args) > 1 else '').startswith('2'):
            super().log_message(fmt, *args)

    def end_headers(self):
        # Without this a rebuild shows you the previous page.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def main():
    args = sys.argv[1:]
    port = 8000
    if '--port' in args:
        port = int(args[args.index('--port') + 1])

    if '--no-build' not in args:
        print('Building…')
        build = subprocess.run([sys.executable, os.path.join(ROOT, 'build.py')],
                               cwd=ROOT)
        if build.returncode != 0:
            sys.exit('\nBuild failed — nothing to serve.')

    if not os.path.isdir(SITE):
        sys.exit('No site/ directory. Run `python build.py` first.')

    handler = functools.partial(Handler, directory=SITE)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        server = socketserver.TCPServer(('127.0.0.1', port), handler)
    except OSError as exc:
        sys.exit(f'\nCould not listen on port {port}: {exc}\n'
                 f'Something else is probably using it — try '
                 f'`python preview.py --port {port + 1}`.')

    url = f'http://127.0.0.1:{port}/'
    print('\n' + '─' * 59)
    print(f' [Context] is at  {url}')
    print(' Ctrl-C to stop.')
    print('─' * 59 + '\n')
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
        server.server_close()


if __name__ == '__main__':
    main()
