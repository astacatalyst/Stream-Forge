# StreamForge — Team Rules

Our working conventions for Git, code review, and collaboration on this project.

## Branching

- `main` is always kept in a working state — nothing gets pushed directly to it.
- Every contributor works on their own branch, named after themselves (e.g. `priya`, `jyoti`, `pooja`).
- Pull from `main` before starting new work to avoid diverging too far.

## Commit & Push

- Commit early and often within your own branch — small, descriptive commits are preferred over one large one.
- Write commit messages that describe *what* changed, e.g. `Add mock /workers endpoint, render dynamic nodes in React Flow`, not vague messages like `update` or `fix`.
- Never commit generated/environment folders: `venv/`, `node_modules/`, `__pycache__/`. Each contributor's folder must include a `.gitignore` covering these before their first commit.

## Pull Requests

- Every feature or fix goes through a Pull Request into `main`, even for the project lead's own work — this keeps the process consistent and gives everyone a chance to review.
- PR titles should be descriptive (e.g. `Week 1: Scaffold FastAPI backend + React Flow dashboard`), not a name or a single word.
- PR descriptions should briefly explain what was built or changed, so a reviewer doesn't have to guess from the diff alone.

## Code Review

- Every PR gets reviewed before merging — even a quick sanity check catches real issues. Example: a review on this project caught a typo (`mport json` instead of `import json`) that would have caused an immediate crash if merged unreviewed.
- Reviewers use GitHub's **Request Changes** for anything that needs fixing before merge, and leave the comment directly on the affected line so the author can find it quickly.
- Once fixes are pushed to the same branch, the PR updates automatically — no need to open a new one.
- Use **Approve** once the code looks correct and complete.

## Merging

- Merge strategy: **Create a merge commit** (not squash or rebase), so the full commit history of each feature is preserved and reviewable later.
- After merging, pull the updated `main` locally before starting the next piece of work: `git checkout main && git pull`.

## Communication

- If someone is blocked waiting on another teammate's work (e.g. a data format, a topic name), that dependency should be stated explicitly and in writing (chat message or PR comment) — not assumed.
- If a teammate is unresponsive, don't block on them indefinitely — continue with mock/placeholder data and swap in real data once available, keeping the eventual integration point clearly documented (see `API_CONTRACT.md`).
- Scope ownership is respected: each person's area (see `PROJECT_ARCHITECTURE.md`) is theirs to build; if work outside that scope is happening, it's flagged and discussed before duplicating effort.