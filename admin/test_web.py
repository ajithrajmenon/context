# -*- coding: utf-8 -*-
"""The backoffice, offline: routing, the lock on the door, and publishing.

No Claude, no git remote, no network, no server. What this checks is the wiring
that the refactor into routers and a service layer could plausibly have broken,
and the two things that must never regress: nothing is reachable without a
session, and a failed publish tells the truth about what it did.

    python -m admin.test_web

Quality of generated content is not in scope here — that is test_pipeline.py for
the wiring and a live run for the writing.
"""
import warnings

warnings.filterwarnings('ignore')

from fastapi.testclient import TestClient        # noqa: E402

from . import publish, session                   # noqa: E402
from .app import app                             # noqa: E402
from .config import PASSWORD, PREFIX             # noqa: E402

# Every page a signed-in editor can open. Kept as one list so a new router
# cannot quietly arrive without being checked.
PAGES = ['/', '/stories', '/generate', '/queue', '/runs']

# Anything that acts rather than renders, with valid form data. The data matters:
# FastAPI validates the request before the handler runs, so posting nothing would
# be turned away as malformed and prove nothing about the lock.
ACTIONS = [
    ('/stories/visibility', {'slug': 'x', 'visible': '0'}),
    ('/publish-site', {}),
    ('/generate', {'goal': 'anything'}),
    ('/draft/1/revise', {'instruction': 'anything'}),
    ('/draft/1/reject', {}),
    ('/draft/1/approve', {}),
]


class Run:
    """Stands in for subprocess.CompletedProcess."""

    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def fake_git(**outcomes):
    """A subprocess runner that answers by git subcommand.

    Returns (run, calls) — `calls` records the argv of everything attempted, so a
    test can assert that a publish stopped before it committed rather than only
    that it reported failure.
    """
    calls = []

    def run(argv, **kw):
        calls.append(argv)
        if argv[0] != 'git':
            return outcomes.get('build', Run(0, 'built 52 stories\n'))
        return outcomes.get(argv[3], Run(0))
    return run, calls


def test_locked_without_a_session():
    client = TestClient(app)
    for path in PAGES + ['/draft/1', '/run/1', '/preview/1/story.html']:
        r = client.get(PREFIX + path, follow_redirects=False)
        assert r.status_code == 303, f'GET {path} was not locked'
        assert r.headers['location'].endswith('/login'), path
    for path, data in ACTIONS:
        r = client.post(PREFIX + path, data=data, follow_redirects=False)
        assert r.status_code == 303, f'POST {path} was not locked ({r.status_code})'
        assert r.headers['location'].endswith('/login'), path

    # The login page and the health check are the only open doors, and health
    # must not leak anything but a count.
    assert client.get(PREFIX + '/login').status_code == 200
    body = client.get(PREFIX + '/health').json()
    assert set(body) == {'ok', 'stories'}, body

    # An unguessable prefix is not access control, but the door should still not
    # be at a guessable address.
    assert client.get('/backoffice/').status_code == 404 or PREFIX == '/backoffice'


def test_password():
    assert not session.password_ok(''), 'an empty password was accepted'
    assert not session.password_ok('wrong')
    assert not session.password_ok(None)
    if PASSWORD:
        assert session.password_ok(PASSWORD)


def test_pages_render():
    """Sign in and open everything. Skipped if the machine has no password set,
    because a fresh clone legitimately has none."""
    if not PASSWORD:
        return 0
    client = TestClient(app)
    r = client.post(PREFIX + '/login', data={'password': PASSWORD},
                    follow_redirects=False)
    assert r.status_code == 303 and r.headers['location'] == PREFIX + '/'

    for path in PAGES:
        r = client.get(PREFIX + path)
        assert r.status_code == 200, f'{path} -> {r.status_code}'
        # The chrome proves the page went through ui.page() rather than being
        # returned as a bare fragment.
        assert 'Sign out' in r.text, f'{path} lost its nav'
        assert 'noindex,nofollow' in r.text, f'{path} is indexable'

    # Signing out must actually invalidate the session server-side, not just drop
    # the cookie in the browser.
    token = client.cookies.get('ctx_admin')
    client.get(PREFIX + '/logout')
    assert not session.authed(_Req({'ctx_admin': token})), \
        'the session still worked after signing out'
    return len(PAGES)


class _Req:
    def __init__(self, cookies):
        self.cookies = cookies


def test_asset_traversal():
    """The preview serves files out of assets/ by name, so it has to refuse a
    name that climbs out of it — admin/.env is one directory up."""
    client = TestClient(app)
    for name in ['../admin/.env', '../../admin/.env', '..%2fadmin%2f.env',
                 '/etc/passwd']:
        r = client.get(f'{PREFIX}/preview/assets/{name}')
        assert r.status_code == 404 or 'CONTEXT_ADMIN' not in r.text, \
            f'{name} escaped the assets directory'


def test_publish_reports_what_it_did():
    """Every way a publish can fail, and what the editor is told.

    This is what the injected runner is for: none of these branches could be
    reached before without an actual broken remote.
    """
    # Build fails -> nothing is committed, and it says so.
    run, calls = fake_git(build=Run(1, '', 'SyntaxError in stories_data.py'))
    ok, log = publish.Repo(run=run).commit_and_push('x')
    assert not ok
    assert 'Nothing was committed' in log
    assert 'SyntaxError' in log, 'the build error was not shown'
    assert not any(c[0] == 'git' for c in calls), 'it committed after a failed build'

    # Nothing changed -> success, and still no commit.
    run, calls = fake_git(status=Run(0, ''))
    ok, log = publish.Repo(run=run).commit_and_push('x')
    assert ok and 'already current' in log
    assert not any('commit' in c for c in calls), 'it committed with no changes'

    # Commit fails -> stop, do not push.
    run, calls = fake_git(status=Run(0, ' M content/x.json'),
                          commit=Run(1, '', 'nothing to commit'))
    ok, log = publish.Repo(run=run).commit_and_push('x')
    assert not ok
    assert not any('push' in c for c in calls), 'it pushed after a failed commit'

    # Push fails -> the commit is local, and the editor is told how to recover.
    run, calls = fake_git(status=Run(0, ' M content/x.json'),
                          push=Run(1, '', 'Permission denied'))
    ok, log = publish.Repo(run=run).commit_and_push('x')
    assert not ok
    assert 'commit is local' in log
    assert 'Permission denied' in log

    # Success names the branch, because Pages only redeploys from one of them.
    run, calls = fake_git(status=Run(0, ' M content/x.json'),
                          **{'rev-parse': Run(0, 'main\n')})
    ok, log = publish.Repo(run=run).commit_and_push('Publish: something')
    assert ok and 'Pushed to main' in log
    pushed = [c for c in calls if 'push' in c][0]
    assert pushed[-2:] == ['origin', 'main'], pushed
    # The message reaches git verbatim.
    committed = [c for c in calls if 'commit' in c][0]
    assert 'Publish: something' in committed

    # A detached head still yields a usable branch name rather than an empty one.
    run, _ = fake_git(status=Run(0, ' M x'), **{'rev-parse': Run(0, '\n')})
    ok, log = publish.Repo(run=run).commit_and_push('x')
    assert ok and 'Pushed to main' in log

    # The build must not be shelled as 'python3': on Windows that name is an App
    # Execution Alias that opens the Microsoft Store instead of running anything.
    run, calls = fake_git()
    publish.Repo(run=run).build()
    assert calls[0][0] != 'python3', 'the build would not run on Windows'
    assert calls[0][1] == 'build.py'


def main():
    test_locked_without_a_session()
    print('locked       every page and action redirects to the login')
    test_password()
    print('password     empty and wrong are both refused')
    opened = test_pages_render()
    print(f'pages        {opened} rendered signed-in, session dies on sign out'
          if opened else 'pages        skipped (no CONTEXT_ADMIN_PASSWORD set)')
    test_asset_traversal()
    print('assets       cannot be climbed out of')
    test_publish_reports_what_it_did()
    print('publish      build, commit and push failures each report correctly')
    print('\nBackoffice wiring OK.')


if __name__ == '__main__':
    main()
