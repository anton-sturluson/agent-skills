#!/usr/bin/env bash
set -euo pipefail

REPOSITORY="anton-sturluson/agent-skills"
REF="${AGENT_SKILLS_REF:-main}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$OPENCLAW_HOME/workspace}"

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
SOURCE_DIR="${AGENT_SKILLS_SOURCE:-}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Required command not found: $1" >&2
    exit 1
  fi
}

install_skills() {
  local source="$1"
  local destination="$2"

  mkdir -p "$destination"

  while IFS= read -r -d '' skill; do
    [[ -f "$skill/SKILL.md" ]] || continue

    local name
    name="$(basename "$skill")"

    mkdir -p "$destination/$name"
    rsync -a --delete "$skill/" "$destination/$name/"
    printf 'Installed %s -> %s\n' "$name" "$destination/$name"
  done < <(find "$source" -mindepth 1 -maxdepth 1 -type d -print0)
}

require_command curl
require_command find
require_command rsync
require_command tar

if [[ -z "$SOURCE_DIR" ]]; then
  printf 'Downloading %s@%s...\n' "$REPOSITORY" "$REF"
  curl -fsSL "https://github.com/$REPOSITORY/archive/$REF.tar.gz" \
    | tar -xz -C "$TEMP_DIR" --strip-components=1
  SOURCE_DIR="$TEMP_DIR"
fi

if [[ ! -d "$SOURCE_DIR/skills/workspace" || ! -d "$SOURCE_DIR/skills/shared" ]]; then
  echo "Invalid agent-skills source: $SOURCE_DIR" >&2
  exit 1
fi

install_skills "$SOURCE_DIR/skills/workspace" "$WORKSPACE/skills"
install_skills "$SOURCE_DIR/skills/shared" "$OPENCLAW_HOME/skills"

printf 'All skills installed successfully.\n'
