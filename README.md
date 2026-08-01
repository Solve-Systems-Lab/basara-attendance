# Basara Attendance

Attendance for this course is taken on a paper sheet — passed along the rows, then retyped into a spreadsheet at night. This repository replaces it, and the whole class builds it together.

**The end state:** a student opens a URL on their phone, marks attendance from inside the classroom, is verified by their own face, and staff ask the data a question in plain English and get a true answer back.

```
backend/     Django + DRF — the API, the data model, face matching, the LLM
frontend/    React + Tailwind — what a student actually touches
docs/        your group's work card, the build brief, the team list, the decisions
```

## Start here

| You want | Go to |
|---|---|
| **Which group am I in, and what is my branch?** | [docs/TEAMS.md](docs/TEAMS.md) |
| **What exactly does MY group build?** | [docs/group-cards.pdf](docs/group-cards.pdf) — one card per group: your files, your tasks, who you wait on |
| **How does it all fit together?** | [docs/brief.pdf](docs/brief.pdf) — architecture, the request flow, and **the API contract** |
| **Who is blocking me?** | [docs/brief.pdf](docs/brief.pdf) — *Order of Work* and *Who Blocks Whom* |
| **Why is the stack what it is?** | [docs/DECISIONS.md](docs/DECISIONS.md) |
| **How do I run it?** | [Running it](#running-it), below |
| **How do I get my work merged?** | [Contributing](#contributing), below |

---

## Three rules

1. **One mark per student per session.** Enforced by a database constraint, not by an `if`. A check followed by a write is a race, and two taps on a slow connection will find it.
2. **The client is never trusted.** Anything a phone can set, a phone can lie about — coordinates, timestamps, the photo itself. The server decides.
3. **Nothing leaves this server.** Attendance photos and face embeddings stay on the class machine. Not S3, not a commercial cloud, not outside India.

---

## Running it

You need **Python 3.12** and **Node 20+**:

```bash
python3.12 --version    # 3.12.x
node --version          # v20 or newer
```

> **Python 3.14 will not work.** `numpy`, `pandas`, `onnxruntime` and `Pillow` are pinned to versions whose newest prebuilt wheels are for Python 3.13. On 3.14 pip falls back to compiling from source — which needs a C++ toolchain you should not need, and `onnxruntime` will simply fail. **Use 3.12** (3.13 also works; 3.12 is the tested one). If it is missing: `brew install python@3.12` on macOS, `sudo apt install python3.12 python3.12-venv` on Ubuntu.

### Backend

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt --timeout 30 --retries 8

cp .env.example .env                 # defaults are fine for local work
python manage.py migrate
python manage.py runserver
```

Check it:

```bash
curl -s localhost:8000/api/health/     # {"ok": true}
```

That one route is all the backend answers today. The other seven are the BE track's first sprint, listed in a comment at the top of `backend/core/urls.py`.

> If `pip install` seems to hang, that is the network, not you — `--timeout 30 --retries 8` makes pip give up on a stalled connection and retry instead of waiting forever.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173
```

Requests to `/api` are proxied to Django on port 8000, so in development the browser sees a single origin and CORS never comes up.

Every screen is a placeholder naming its owning group and what it has to do. That is deliberate — the scaffold proves the router, the build and the type-checker all work, and leaves the screens to you.

```bash
npm run typecheck                    # must pass before you open a pull request
npm run build
```

---

## Layout

```
backend/
  config/           settings, root URLconf                    BE
  core/             models (finished), API, auth              BE
  presence/         campus IP, session codes, audit log       SPD
  faceid/           ONNX embeddings, cosine, thresholds       ML
  llm/  agent/      Claude client, ask endpoint, tool loop    ML
  evals/  analysis/ eval set, pandas analysis                 ML
  scrape/           roster scraping                           ML
  deploy/           Caddy, systemd                            SPD
  tests/            pytest

frontend/
  src/app/                    screens, routing, services      FE
  src/styles/                 design tokens, theme            UI/UX
  src/app/components/ui/      shared primitives               UI/UX

docs/               group-cards.pdf, brief.pdf, TEAMS.md, DECISIONS.md
```

`backend/core/models.py` is **already written** — nine models covering students, sessions, attendance records, photos, coordinates, face scores, session codes and the audit log. Read it before you write anything. Do not rewrite it.

---

## Contributing

### Branches

```
main        protected — deploys to production
  staging   release candidates
    dev     integration; every pull request targets this
      team/<group-slug>       one per group, already created
```

**If you have push access**, your branch already exists — check it out, do not create it:

```bash
git clone git@github.com:Solve-Systems-Lab/basara-attendance.git
cd basara-attendance
git checkout team/<your-group-slug>      # see docs/TEAMS.md
# work, commit
git push origin team/<your-group-slug>
```

**If you do not have push access yet** — likely on day one, before usernames have been collected — fork it and open the pull request from your fork:

```bash
gh repo fork --clone
git checkout -b team/<your-group-slug>
# work, commit
git push -u origin team/<your-group-slug>
gh pr create --base dev
```

Both routes end in the same place: a pull request against `dev`, reviewed by a group from another track.

### Before you open a pull request

- `npm run typecheck` and `npm run build` pass, if you touched the frontend
- `pytest` passes, if you touched Python
- No secrets. `git diff --cached | grep -iE 'sk-ant|AKIA|password|secret'` comes back empty
- Your commit message says what changed and why, not `update`

---

## What must never be committed

`.gitignore` covers these, but understand *why* rather than trusting the file:

| Never commit | Why |
|---|---|
| `.env` | Secrets. The single most important line in `.gitignore`. |
| `backend/media/` | Attendance photos and face enrolment images. **Biometric data belonging to your classmates.** |
| `db.sqlite3` | Real student records. |
| `*.onnx` | Large binaries; fetch them from the class server. |

Names, roll numbers and email addresses do not belong in this repository either. It is public and permanent — which is why `docs/TEAMS.md` lists groups and branches but no people.

The reference implementation this project ports from committed live AWS credentials and a database of real employee names, phone numbers and GPS coordinates. That is one careless `git add -A` away from happening here.

---

## Reference implementation

You have been given a **working production attendance system** on this same stack to port from. It is genuinely useful and genuinely flawed: plaintext passwords, a login token generated and then never checked again, and every endpoint open to the world. Its own authors documented all of it.

Most of you have never read production code before. You are about to read some, find the holes yourselves, and fix them.

**Port from it. Do not copy it.**
