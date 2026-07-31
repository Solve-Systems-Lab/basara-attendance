# Decisions — Basara Attendance App

Session log for the class build. Written 2026-07-31, in class.
Read this before reversing anything below; each entry records the cost that was accepted, not just the choice.

---

## 0. Why we are building this

Attendance for this course is taken on a paper sheet. Sixty-odd rows, student 1 to student n, filled in by hand and passed along the row. Someone on the team then sits at night and retypes it into an Excel sheet.

So the course builds the thing that fixes the course. Students mark their own attendance, from their own phone, in the room. The retyping goes away, and every student has shipped the system that made it go away.

The end state, said in one sentence:

> A student opens a URL on their phone, marks attendance from inside the classroom, is verified by their own face, and staff ask the data a question in plain English and get a true answer back.

Three non-negotiables that everything else hangs off:

1. One mark per student per session. Enforced in the database, not in a `if` statement.
2. The client is never trusted. Anything a phone can set, a phone can lie about.
3. Nothing leaves the class server. Photos and face embeddings stay on the box.

---

## 1. Stack: React + Tailwind + shadcn on the front, DRF + JWT on the back

**Decision.** Vite + React 18 + TypeScript + Tailwind v4 + shadcn/ui + react-router v7 for the frontend. Django 5.1 + DRF + `djangorestframework-simplejwt` for the backend.

**This reverses a decision already argued in `INSTRUCTOR-PREP.md` §1c**, which says to delete the React frontend entirely and port six screens to Django templates — "the single largest time saving available, and it removes the most likely deployment catastrophe."

**Why we overrode it.** The roster self-selected into categories. Five students picked FE and eleven picked UI/UX. On the Django-templates path those sixteen students have roughly forty lines of vanilla JS between them and nothing else. That is not a course. Separately, `pmu_ap_itda/pmutwd_attendance/fe` already contains a working React app on exactly this stack, so this is a **port, not a greenfield build** — which is what makes it affordable at all.

**Cost accepted knowingly.** `npm install` on ~100 laptops over campus WiFi. CORS configuration. Token refresh, which the templates path would not need. A Node toolchain on modest machines. If the WiFi makes `npm install` impossible on day one, the fallback is a local wheelhouse/registry mirror on the class server — not abandoning the frontend.

---

## 2. Auth: SimpleJWT, and `django.contrib.auth` underneath

**Decision.** JWT access + refresh via `djangorestframework-simplejwt`. Passwords go through `django.contrib.auth`. No second factor.

**Why it is worth teaching rather than hand-waving.** The reference implementation at `pmu_ap_itda/pmutwd_attendance/be` gets this comprehensively wrong, and every mistake is legible:

| What it does | Where |
|---|---|
| Compares passwords as plaintext strings — `Login.objects.get(user_name=u, password=p)` | `be/apps/attendance/views.py:47` |
| Returns `str(uuid.uuid4())` as a "token", never stores it, never checks it again | `views.py:48` |
| Frontend dutifully sends that token as `Authorization: Bearer` on every request, forever | `fe/src/app/services/api.ts:80` |
| `AllowAny` on all 27 endpoints; no view ever reads `request.user` | throughout `views.py` |
| Identity arrives as a `user_id` **form field**, so anyone can mark attendance for anyone | `serializers.py`, `MarkAttendanceAPI` |

It looks authenticated end to end. It is theatre. The repo's own `PLATFORM_FRAMEWORK_ANALYSIS.md` documents all of it, so the authors knew.

The sharpest thread to pull: that project's stakeholder asked for `GET /api/auth/me`. It is five lines. It was **impossible to build there**, because the token meant nothing and there was no "current user" for the server to resolve. Auth is architecture, not a feature you add later.

---

## 3. Roster: 106 students in 19 groups

**Decision.** Use the class roster as-is. The normalised version is held privately by the instructor; [TEAMS.md](TEAMS.md) carries the part students need — group, track, branch, member count. Names and email addresses are deliberately kept out of this public repository.

**Correction on the record.** The working assumption in the room was 60 students in 14 groups. The roster actually holds **106 students across 19 group mailboxes**, sized 3 to 10. Group identity is the shared mailbox, not the `Group` column — that column is filled in for only three groups.

GRP10 has ten members, five tagged BE and five tagged ML. That looks like two teams sharing one mailbox. It stays one group for now; split it into two branches if it does not function as one team.

---

## 4. Tracks: assigned by `Catagory`, then rebalanced

**Decision.** Five tracks. Assignment starts from each group's self-selected `Catagory`, then rebalanced with the instructor's authorisation.

**Why rebalancing was necessary.** Self-selection produced ML 43, SPD 18, BE 16, UI/UX 11, FE 5, blank 13. Forty-three students on one feature and five carrying an entire frontend is not a workable split.

| Track | Groups | Students |
|---|---|---|
| **BE** — Django, DRF, JWT, data model | GRP5, GRP7, GRP10, GRP12 | 24 |
| **FE** — React, router, camera, geolocation | GRP8, BALAJI, GRP14, DRAGONS | 19 |
| **UI/UX** — design system, tokens, components | MINIONS, GRP6, ASTERIX | 16 |
| **ML/AI** — face embeddings, LLM ask, evals | ANUSHA, NEXAAI, GRP4, FEMMEFORCE, GRP11 | 29 |
| **SPD** — presence signals, deploy, CI/CD | BHUVANESHWARI, MINIBYTES, ROCKSTARS | 18 |

Moves made: BALAJI and GRP14 from ML to FE. The three groups with a blank category — DRAGONS, GRP12, ASTERIX — went to FE, BE and UI/UX respectively, where the need was.

ML keeps the most groups on purpose: it carries face recognition, the LLM ask path, the agent loop, and evals. That is genuinely the deepest track, not a dumping ground.

---

## 5. Database: SQLite

**Decision.** SQLite, single file, on the class server.

**Why.** 106 students × 5 subjects × ~36 sessions ≈ 19,000 attendance rows. One writer, one box, no concurrency story to speak of. Postgres adds an install step per team and buys nothing at this size. Recorded here so it reads as a decision rather than an omission — a student will ask, and "we chose SQLite because the working set is 19k rows on one machine" is the answer.

---

## 6. Presence signals: two gates, one log

**Decision.** Gate on campus IP and a rotating projector code. Record GPS and never gate on it.

| Signal | Indoors? | Room-level? | Cost to fake | Verdict |
|---|---|---|---|---|
| Source IP in `CAMPUS_CIDR` | yes | no | must be on the campus network | **gate** |
| Rotating projector code, 60 s TTL, single use | yes | **yes — you must see the screen** | WhatsApp it; TTL mitigates | **gate** |
| GPS lat/lng + accuracy | no | no | trivial, devtools | **log only** |

`haversine()` gets written, tested, and deliberately never wired into the accept/reject path. A student who can explain why that function exists and is unused has understood the day.

Two traps that are load-bearing:
- Behind Caddy, `request.META["REMOTE_ADDR"]` is the **proxy**. Read `X-Forwarded-For`.
- `getUserMedia()` and the Geolocation API are secure-context only. On plain HTTP `navigator.mediaDevices` is `undefined`, so the failure surfaces as a `TypeError` that reads like an application bug. No TLS, no camera, no Days 7–8.

---

## 7. Face recognition: local ONNX, not a vision API

**Decision.** ONNX Runtime with a small detector plus MobileFaceNet/ArcFace producing 512-d embeddings, cosine similarity, per-team threshold.

**Why not a hosted vision model.** Two independent reasons, per `INSTRUCTOR-PREP.md`. Anthropic's usage policy prohibits facial recognition. And decisively for teaching: **a vision API cannot return a similarity score.** No score means no threshold, no false-accept/false-reject trade-off — and that trade-off *is* the lesson.

Each group picks its own threshold and defends it out loud. "I chose 0.62 because a false reject costs a student their exam eligibility and a false accept costs the institution very little" is the sentence we are aiming at.

Liveness gets exactly one cheap mitigation: two frames 800 ms apart, reject if byte-identical or cosine ≈ 1.000. Then hold a photo of a face up to the camera and watch it pass anyway. A photo of a face is a face.

---

## 8. Repo and branches

One repo, `basara-attendance`. Note it is **not currently a git repo** — `git init` is step zero.

```
main        protected, deploys to prod
  staging   release candidates
    dev     integration; all PRs target this
      team/<group-slug>    one branch per group, e.g. team/femmeforce
```

PRs go `team/*` → `dev`, reviewed by another group in the same track. `dev` → `staging` → `main` on the instructor's call. CI on PR: lint, `pytest`, `vite build`.

The reference repo's `deploy-backend.yml` is `git pull && migrate && restart gunicorn` against a live box with a SQLite file in the working tree — no tests, no backup, no rollback. SPD improves on it and writes down why.

---

## 9. Things deliberately not done

- **No second factor.** Student ID and password. The complexity budget is spent on faces and presence signals.
- **No S3.** Photos and enrolment images stay in local `media/`. The reference uses a public, unsigned, guessable S3 key (`attendance/{y}/{m}/{d}/{username}.jpeg`) — do not copy that.
- **No RAG.** The Day-6 query functions *are* the retrieval.
- **No Postgres, no Celery, no Redis.** Nothing here needs them.

---

## 10. Open items

- GitHub org and repo URL — placeholder `<repo-url>` in the brief until confirmed.
- Whether GRP10 (10 people) splits into two sub-teams on separate branches.
- Class server hostname, `CAMPUS_CIDR` value, and the LLM proxy URL.
- `WORKSHOP.md` and `READINGS.md` are on different day numbering (off by one). Pick one before Day 3.

---

## Reference material

`../../pmu_ap_itda/pmutwd_attendance/` is a working production attendance system on this stack. Port from it; do not copy it wholesale.

**Do not copy into the class repo:** `be/.env` (live AWS keys), `be/db.sqlite3` (real employee names, phone numbers, GPS coordinates, plaintext passwords), `be/venv/`, `credentials.xlsx`, `SSH_CREDENTIALS.md`.

**Worth reading in it:** `PLATFORM_FRAMEWORK_ANALYSIS.md` — an honest defect list written by the people who shipped it. Real code review of real production code.
