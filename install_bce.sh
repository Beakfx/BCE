#!/usr/bin/env bash
set -e

log() {
    echo "[BCE] $1"
}

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLAME_DEST="/opt/Autodesk/shared/python/BCE"
USER_ROOT="$HOME/bce"

cd "$REPO_ROOT"

required_dirs=("docs" "flame_python" "matchbox" "templates")

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        log "Missing required source folder: $dir"
        log "Please run this installer from the BCE repo root."
        exit 1
    fi
done

if [ ! -d ".git" ]; then
    log "Installing from archive (no .git) — continuing from: $REPO_ROOT"
fi

log "Installing Flame Python hooks..."
sudo mkdir -p "$FLAME_DEST"
sudo rsync -a flame_python/ "$FLAME_DEST/"

log "Creating user BCE folders..."
mkdir -p \
    "$USER_ROOT/docs" \
    "$USER_ROOT/matchbox" \
    "$USER_ROOT/templates" \
    "$USER_ROOT/templates/write_nodes" \
    "$USER_ROOT/templates/gui_versions" \
    "$USER_ROOT/config" \
    "$USER_ROOT/bce_jobs"

log "Installing docs..."
rsync -a docs/ "$USER_ROOT/docs/"

log "Installing matchbox files..."
rsync -a matchbox/ "$USER_ROOT/matchbox/"

log "Installing templates..."
rsync -a templates/ "$USER_ROOT/templates/"

log "Install complete."
log "Flame hooks installed to: $FLAME_DEST"
log "User files installed to: $USER_ROOT"
log "In Flame, open BCE > Setup and Config."
log "Set Work Root to: $USER_ROOT/bce_jobs"
log "Set Templates Dir to: $USER_ROOT/templates"
