---
name: push-git-remote
description: "Commit, push, open a PR, merge, and clean up in one flow. Use when: (1) pushing local changes to a remote branch and merging via PR, (2) finalizing work on a feature branch or worktree, (3) asked to 'push this', 'open a PR', 'merge this branch', or 'ship it'. Handles branch creation, commit, push, PR creation, merge, and post-merge cleanup (checkout main or remove worktree)."
---

# Push Git Remote

End-to-end flow: branch → commit → push → PR → merge → cleanup.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`).
- Remote `origin` configured and pushable.

## Workflow

### 1. Ensure a feature branch

```bash
# If on main/master, create and switch to a new branch
CURRENT=$(git branch --show-current)
if [ "$CURRENT" = "main" ] || [ "$CURRENT" = "master" ]; then
  git checkout -b <branch-name>
fi
```

Branch naming: use `feat/`, `fix/`, or `chore/` prefixes with kebab-case (e.g. `feat/add-auth`).

### 2. Stage and commit

```bash
# Stage specified files, or all changes if none specified
git add <files>        # or: git add -A
git commit -m "<type>: <concise summary>"
```

- Use conventional commit messages (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`).
- If the user specifies a commit message, use it verbatim.

### 3. Push

```bash
git push -u origin <branch-name>
```

### 4. Create PR

```bash
gh pr create --title "<same as commit or user-provided>" --body "<brief description of changes>"
```

- If the user provides a PR title or description, use those.
- Otherwise derive from the commit message.
- Target branch defaults to `main` (or `master` if that's the default branch).

### 5. Merge

```bash
gh pr merge --squash --delete-branch
```

- Default to squash merge. Use `--merge` or `--rebase` only if the user requests it.
- `--delete-branch` removes the remote branch after merge.

### 6. Cleanup

Detect whether we're in a worktree or a regular checkout:

```bash
# Check if this is a worktree (git worktree list shows multiple entries)
WORKTREE_DIR=$(git rev-parse --show-toplevel)
MAIN_WORKTREE=$(git worktree list --porcelain | head -1 | sed 's/worktree //')

if [ "$WORKTREE_DIR" != "$MAIN_WORKTREE" ]; then
  # In a worktree — move out, then remove it
  cd "$MAIN_WORKTREE"
  git worktree remove "$WORKTREE_DIR"
  # Also delete the local branch
  git branch -d <branch-name>
else
  # Regular checkout — switch back to default branch
  DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
  git checkout "$DEFAULT"
  git pull
  git branch -d <branch-name>
fi
```

## Error handling

- If `gh pr create` fails due to no commits ahead, confirm the branch has been pushed.
- If merge fails due to conflicts or required reviews, report to the user and stop.
- If worktree removal fails (dirty files), warn the user before force-removing.

## Rules

- Always confirm with the user before merging if there are open review comments or failing CI checks.
- Never force-push unless explicitly asked.
- Never delete `main` or `master`.
