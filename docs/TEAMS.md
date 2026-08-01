# Teams and branches

Twenty groups, 82 students, five tracks. Find your group, check out your branch,
then read your track page in [`brief.pdf`](brief.pdf).

> Student names and email addresses are deliberately **not** in this repository.
> It is public, indexed, and effectively permanent. The printed brief handed out in
> class carries the full roster. Apply the same rule to everything you commit.

| Group | Track | Your branch | Members |
|---|---|---|---|
| **GRP5** | BE | `team/grp5` | 6 |
| **GRP7** | BE | `team/grp7` | 5 |
| **CLAUDE** | BE | `team/claude` | 4 |
| **NEURALTEAM** | BE | `team/neuralteam` | 3 |
| **DRAGONS** | FE | `team/dragons` | 5 |
| **ASTERIX** | FE | `team/asterix` | 5 |
| **GRP8** | FE | `team/grp8` | 5 |
| **GRP14** | FE | `team/grp14` | 4 |
| **MINIONS** | UI/UX | `team/minions` | 4 |
| **AGENTS** | UI/UX | `team/agents` | 4 |
| **NEXAAI** | UI/UX | `team/nexaai` | 2 |
| **GRP4** | ML | `team/grp4` | 5 |
| **GRP11** | ML | `team/grp11` | 5 |
| **ANUSHA** | ML | `team/anusha` | 4 |
| **BALAJI** | ML | `team/balaji` | 4 |
| **FEMMEFORCE** | ML | `team/femmeforce` | 3 |
| **BHUVANESHWARI** | SPD | `team/bhuvaneshwari` | 5 |
| **ROCKSTARS** | SPD | `team/rockstars` | 3 |
| **MINIBYTES** | SPD | `team/minibytes` | 3 |
| **GRP12** | SPD | `team/grp12` | 3 |

## What each track owns

| Track | Focus | Directories |
|---|---|---|
| **BE** | Backend — Django, DRF, JWT | `backend/core/` `backend/config/` |
| **FE** | Frontend — React, router, camera | `frontend/src/app/` `frontend/src/services/` |
| **UI/UX** | UI/UX — design system | `frontend/src/styles/` `frontend/src/app/components/ui/` |
| **ML** | ML & AI — faces, LLM, evals | `backend/faceid/` `llm/` `agent/` `evals/` `analysis/` `core/queries.py` |
| **SPD** | Platform — presence, deploy, CI | `backend/presence/` `backend/deploy/` `.github/workflows/` |

## Working on your branch

```bash
git checkout team/<your-group-slug>    # already exists — do not create it
git pull
# ... work, commit ...
git push origin team/<your-group-slug>
```

All twenty branches already exist and point at the first commit, so the slug above
is guaranteed to match the one on your printed brief. Open your pull request against
`dev`, and have a group from another track review it.

If you do not have push access yet, see **Contributing** in the
[README](../README.md) — the fork-and-pull-request route works with no setup at all.
