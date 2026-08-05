# -*- coding: utf-8 -*-
"""The backoffice database.

SQLite, because the whole point of this project is that it runs anywhere with
Python and nothing else. The database is the *working* store — drafts, the
approval queue, run logs, audit. It is not what the site reads.

The site reads JSON files in `content/`, written only at publish time. So the
flow is one-directional and every published change is a git commit somebody
can read:

    research run  ->  SQLite draft  ->  approval  ->  content/*.json  ->  push
                                                          |
                                                    build.py reads it
"""
import json
import os
import secrets
import sqlite3
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get('CONTEXT_DB', os.path.join(ROOT, 'admin', 'context.db'))

SCHEMA = """
CREATE TABLE IF NOT EXISTS draft (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  slug        TEXT NOT NULL,
  lens        TEXT NOT NULL DEFAULT 'What',
  domain      TEXT NOT NULL DEFAULT 'General',
  title       TEXT NOT NULL DEFAULT '',
  status      TEXT NOT NULL DEFAULT 'draft',   -- draft|queued|approved|published|rejected
  story_json  TEXT NOT NULL DEFAULT '{}',
  paper_json  TEXT NOT NULL DEFAULT '{}',
  notes       TEXT NOT NULL DEFAULT '',
  created_at  REAL NOT NULL,
  updated_at  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS run (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  goal        TEXT NOT NULL,
  lens_hint   TEXT NOT NULL DEFAULT '',
  stage       TEXT NOT NULL DEFAULT 'queued',
  state       TEXT NOT NULL DEFAULT 'running',  -- running|done|failed
  error       TEXT NOT NULL DEFAULT '',
  draft_id    INTEGER,
  cost_in     INTEGER NOT NULL DEFAULT 0,
  cost_out    INTEGER NOT NULL DEFAULT 0,
  created_at  REAL NOT NULL,
  updated_at  REAL NOT NULL
);

-- Every stage's full output, kept so a human can audit what the agents did
-- rather than trusting the final draft on faith. This is the same principle
-- as the papers behind the stories.
CREATE TABLE IF NOT EXISTS run_stage (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id      INTEGER NOT NULL,
  name        TEXT NOT NULL,
  output      TEXT NOT NULL DEFAULT '',
  seconds     REAL NOT NULL DEFAULT 0,
  created_at  REAL NOT NULL
);

-- A live tail of what the current agent is doing — "searching for X", "reading
-- Y" — so a run in progress shows something more honest than a spinner. This is
-- deliberately not the record: run_stage holds each agent's real, complete
-- output once it lands. This table is a rolling window (see PROGRESS_KEEP)
-- that exists only so a person watching a run does not stare at nothing for
-- three minutes and then see one wall of text.
CREATE TABLE IF NOT EXISTS run_progress (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id      INTEGER NOT NULL,
  stage       TEXT NOT NULL,
  text        TEXT NOT NULL,
  created_at  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS edit (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  draft_id    INTEGER NOT NULL,
  prompt      TEXT NOT NULL,
  before_json TEXT NOT NULL,
  after_json  TEXT NOT NULL,
  created_at  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS audit (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  action      TEXT NOT NULL,
  detail      TEXT NOT NULL DEFAULT '',
  created_at  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS session (
  token       TEXT PRIMARY KEY,
  created_at  REAL NOT NULL
);
"""


def connect():
    db = sqlite3.connect(DB_PATH, timeout=20)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA foreign_keys=ON')
    return db


def init():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with connect() as db:
        db.executescript(SCHEMA)


# ---------------------------------------------------------------- sessions

SESSION_TTL = 60 * 60 * 12


def new_session():
    tok = secrets.token_urlsafe(32)
    with connect() as db:
        db.execute('INSERT INTO session (token, created_at) VALUES (?, ?)',
                   (tok, time.time()))
    return tok


def session_ok(tok):
    if not tok:
        return False
    with connect() as db:
        row = db.execute('SELECT created_at FROM session WHERE token = ?',
                         (tok,)).fetchone()
        if not row:
            return False
        if time.time() - row['created_at'] > SESSION_TTL:
            db.execute('DELETE FROM session WHERE token = ?', (tok,))
            return False
    return True


def drop_session(tok):
    with connect() as db:
        db.execute('DELETE FROM session WHERE token = ?', (tok,))


# ---------------------------------------------------------------- drafts

def create_draft(slug, lens, domain, title, story, paper, notes=''):
    now = time.time()
    with connect() as db:
        cur = db.execute(
            'INSERT INTO draft (slug, lens, domain, title, status, story_json,'
            ' paper_json, notes, created_at, updated_at)'
            " VALUES (?, ?, ?, ?, 'queued', ?, ?, ?, ?, ?)",
            (slug, lens, domain, title, json.dumps(story), json.dumps(paper),
             notes, now, now))
        return cur.lastrowid


def get_draft(draft_id):
    with connect() as db:
        return db.execute('SELECT * FROM draft WHERE id = ?', (draft_id,)).fetchone()


def list_drafts(status=None):
    q = 'SELECT * FROM draft'
    args = ()
    if status:
        q += ' WHERE status = ?'
        args = (status,)
    q += ' ORDER BY updated_at DESC'
    with connect() as db:
        return db.execute(q, args).fetchall()


def update_draft(draft_id, **fields):
    if not fields:
        return
    cols, args = [], []
    for k, v in fields.items():
        cols.append(f'{k} = ?')
        args.append(json.dumps(v) if k.endswith('_json') and not isinstance(v, str) else v)
    args += [time.time(), draft_id]
    with connect() as db:
        db.execute(f'UPDATE draft SET {", ".join(cols)}, updated_at = ? WHERE id = ?', args)


def delete_draft(draft_id):
    with connect() as db:
        db.execute('DELETE FROM draft WHERE id = ?', (draft_id,))


def record_edit(draft_id, prompt, before, after):
    with connect() as db:
        db.execute('INSERT INTO edit (draft_id, prompt, before_json, after_json,'
                   ' created_at) VALUES (?, ?, ?, ?, ?)',
                   (draft_id, prompt, json.dumps(before), json.dumps(after), time.time()))


def draft_edits(draft_id):
    with connect() as db:
        return db.execute('SELECT * FROM edit WHERE draft_id = ? ORDER BY created_at DESC',
                          (draft_id,)).fetchall()


# ---------------------------------------------------------------- runs

def create_run(goal, lens_hint):
    now = time.time()
    with connect() as db:
        cur = db.execute('INSERT INTO run (goal, lens_hint, created_at, updated_at)'
                         ' VALUES (?, ?, ?, ?)', (goal, lens_hint, now, now))
        return cur.lastrowid


def update_run(run_id, **fields):
    cols, args = [], []
    for k, v in fields.items():
        cols.append(f'{k} = ?')
        args.append(v)
    args += [time.time(), run_id]
    with connect() as db:
        db.execute(f'UPDATE run SET {", ".join(cols)}, updated_at = ? WHERE id = ?', args)


def add_tokens(run_id, tin, tout):
    with connect() as db:
        db.execute('UPDATE run SET cost_in = cost_in + ?, cost_out = cost_out + ?,'
                   ' updated_at = ? WHERE id = ?', (tin, tout, time.time(), run_id))


def get_run(run_id):
    with connect() as db:
        return db.execute('SELECT * FROM run WHERE id = ?', (run_id,)).fetchone()


def list_runs(limit=40):
    with connect() as db:
        return db.execute('SELECT * FROM run ORDER BY created_at DESC LIMIT ?',
                          (limit,)).fetchall()


def add_stage(run_id, name, output, seconds):
    with connect() as db:
        db.execute('INSERT INTO run_stage (run_id, name, output, seconds, created_at)'
                   ' VALUES (?, ?, ?, ?, ?)', (run_id, name, output, seconds, time.time()))


def run_stages(run_id):
    with connect() as db:
        return db.execute('SELECT * FROM run_stage WHERE run_id = ? ORDER BY id',
                          (run_id,)).fetchall()


# A live status feed, not a log — old lines are worth nothing once newer ones
# exist, so each insert prunes the run back to its most recent window rather
# than growing forever across a long, chatty research stage.
PROGRESS_KEEP = 80


def add_progress(run_id, stage, text):
    with connect() as db:
        db.execute('INSERT INTO run_progress (run_id, stage, text, created_at)'
                   ' VALUES (?, ?, ?, ?)', (run_id, stage, text, time.time()))
        db.execute(
            'DELETE FROM run_progress WHERE run_id = ? AND id NOT IN '
            '(SELECT id FROM run_progress WHERE run_id = ? ORDER BY id DESC LIMIT ?)',
            (run_id, run_id, PROGRESS_KEEP))


def run_progress(run_id, stage=None):
    q = 'SELECT * FROM run_progress WHERE run_id = ?'
    args = [run_id]
    if stage:
        q += ' AND stage = ?'
        args.append(stage)
    q += ' ORDER BY id'
    with connect() as db:
        return db.execute(q, args).fetchall()


# ---------------------------------------------------------------- audit

def log(action, detail=''):
    with connect() as db:
        db.execute('INSERT INTO audit (action, detail, created_at) VALUES (?, ?, ?)',
                   (action, detail, time.time()))


def audit_tail(limit=60):
    with connect() as db:
        return db.execute('SELECT * FROM audit ORDER BY created_at DESC LIMIT ?',
                          (limit,)).fetchall()
