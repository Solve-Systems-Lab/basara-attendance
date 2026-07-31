# Teams and branches

Nineteen groups, 106 students, five tracks. Find your group, check out your branch,
then read your track page in [`docs/brief.pdf`](docs/brief.pdf).

> Student names and email addresses are deliberately **not** in this repository.
> It is public, indexed, and effectively permanent. The printed brief handed out in
> class carries the full roster. Apply the same rule to everything you commit.

| Group | Track | Your branch | Members |
|---|---|---|---|
| **GRP5** | BE | `team/grp5` | 6 |
| **GRP7** | BE | `team/grp7` | 5 |
| **GRP12** | BE | `team/grp12` | 3 |
| **GRP10** | BE | `team/grp10` | 10 |
| **BALAJI** | FE | `team/balaji` | 5 |
| **DRAGONS** | FE | `team/dragons` | 5 |
| **GRP14** | FE | `team/grp14` | 4 |
| **GRP8** | FE | `team/grp8` | 5 |
| **MINIONS** | UI/UX | `team/minions` | 5 |
| **GRP6** | UI/UX | `team/grp6` | 6 |
| **ASTERIX** | UI/UX | `team/asterix` | 5 |
| **ANUSHA** | ML | `team/anusha` | 6 |
| **NEXAAI** | ML | `team/nexaai` | 5 |
| **GRP4** | ML | `team/grp4` | 5 |
| **FEMMEFORCE** | ML | `team/femmeforce` | 8 |
| **GRP11** | ML | `team/grp11` | 5 |
| **BHUVANESHWARI** | SPD | `team/bhuvaneshwari` | 5 |
| **MINIBYTES** | SPD | `team/minibytes` | 8 |
| **ROCKSTARS** | SPD | `team/rockstars` | 5 |

## What each track owns

| Track | Focus | Directories |
|---|---|---|
| **BE** | Backend — Django, DRF, JWT | `core/` `config/` |
| **FE** | Frontend — React, router, camera | `frontend/src/app/` `frontend/src/services/` |
| **UI/UX** | UI/UX — design system | `frontend/src/styles/` `frontend/src/app/components/ui/` |
| **ML** | ML & AI — faces, LLM, evals | `faceid/` `llm/` `agent/` `evals/` `analysis/` `core/queries.py` |
| **SPD** | Platform — presence, deploy, CI | `presence/` `deploy/` `.github/workflows/` |

## Working on your branch

```bash
git checkout team/<your-group-slug>    # already exists — do not create it
git pull
# ... work, commit ...
git push origin team/<your-group-slug>
```

All nineteen branches already exist and point at the first commit, so the slug above
is guaranteed to match the one on your printed brief. Open your pull request against
`dev`, and have a group from another track review it.

If you do not have push access yet, see **Contributing** in the
[README](README.md) — the fork-and-pull-request route works with no setup at all.
