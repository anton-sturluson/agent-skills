---
name: git-worktree
description: "Create and manage git worktrees for feature branches and experiments. Use when: (1) asked to create a worktree, (2) asked to implement a feature or run an experiment in isolation, (3) need parallel development on multiple branches, (4) spawning a coding agent for a feature that should not touch the main checkout. Worktrees are stored in the project's `.worktrees/` folder."
---

# Git Worktree

Manage worktrees inside each project's `.worktrees/` directory.

## Worktree location convention

All worktrees live under `.worktrees/` relative to the project root:

```
/Users/charlie-buffet/Documents/<project>/
├── .worktrees/
│   ├── feat-add-auth/
│   └── experiment-new-parser/
├── src/
└── ...
```

## Creating a worktree

```bash
PROJECT_ROOT="<project-path>"
BRANCH="feat/<name>"          # or experiment/<name>, fix/<name>
WORKTREE_NAME="<kebab-name>"  # matches branch without prefix slashes

# Ensure .worktrees directory exists
mkdir -p "$PROJECT_ROOT/.worktrees"

# Ensure .worktrees is gitignored
grep -qxF '.worktrees/' "$PROJECT_ROOT/.gitignore" 2>/dev/null || echo '.worktrees/' >> "$PROJECT_ROOT/.gitignore"

# Create the worktree with a new branch from current HEAD
cd "$PROJECT_ROOT"
git worktree add -b "$BRANCH" ".worktrees/$WORKTREE_NAME" HEAD
```

- Branch naming: `feat/`, `fix/`, `experiment/`, `chore/` prefix + kebab-case.
- Worktree folder name: the descriptive part without slash (e.g. branch `feat/add-auth` → folder `feat-add-auth`).
- If the branch already exists, use `git worktree add ".worktrees/$WORKTREE_NAME" "$BRANCH"` (no `-b`).

## After creation

- If the project uses a package manager, install dependencies in the worktree:
  ```bash
  cd "$PROJECT_ROOT/.worktrees/$WORKTREE_NAME"
  # Detect and run the right install
  [ -f pnpm-lock.yaml ] && pnpm install
  [ -f yarn.lock ] && yarn install
  [ -f package-lock.json ] && npm install
  ```
- When spawning a coding agent (Codex, Claude Code, etc.), set `workdir` to the worktree path.

## Listing worktrees

```bash
cd "$PROJECT_ROOT" && git worktree list
```

## Removing a worktree

After the work is merged or abandoned:

```bash
cd "$PROJECT_ROOT"
git worktree remove ".worktrees/$WORKTREE_NAME"
git branch -d "$BRANCH"   # delete the local branch if merged
```

If the worktree has uncommitted changes, warn the user before using `--force`.

## Rules

- Always create `.worktrees/` if it doesn't exist.
- Always add `.worktrees/` to `.gitignore` if not already there.
- Never create worktrees outside the project's `.worktrees/` folder.
- When asked to "implement a feature" or "run an experiment", default to creating a worktree unless the user says to work directly on the current branch.
- Pair with the `push-git-remote` skill for the commit → PR → merge → cleanup flow.
