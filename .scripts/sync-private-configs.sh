#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Resolve the project root (one level up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Default configuration
REMOTE_HOST=""
DIRECTION="push"
REMOTE_PATH=""

usage() {
    echo "Usage: $0 [options] <remote-host>"
    echo ""
    echo "Options:"
    echo "  -d, --direction <push|pull>   Sync direction (default: push)"
    echo "  -p, --path <remote-path>      Remote project path (default: same as local)"
    echo "  -h, --help                    Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 100.115.22.44"
    echo "  $0 --direction pull 100.115.22.44"
    exit 1
}

# Parse CLI options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--direction)
            DIRECTION="$2"
            shift 2
            ;;
        -p|--path)
            REMOTE_PATH="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$REMOTE_HOST" ]]; then
                REMOTE_HOST="$1"
                shift
            else
                echo "Error: Unknown argument: $1"
                usage
            fi
            ;;
    esac
done

if [[ -z "$REMOTE_HOST" ]]; then
    echo "Error: Remote host (Tailscale IP/hostname) is required."
    usage
fi

if [[ "$DIRECTION" != "push" && "$DIRECTION" != "pull" ]]; then
    echo "Error: Direction must be either 'push' or 'pull'."
    usage
fi

# Default remote path to match local path
if [[ -z "$REMOTE_PATH" ]]; then
    REMOTE_PATH="$PROJECT_ROOT"
fi

# List of directories to sync
SYNC_DIRS=(
    ".private"
)

echo "=== Private Configuration Sync ==="
echo "Remote Host: $REMOTE_HOST"
echo "Direction:   $DIRECTION"
echo "Local Path:  $PROJECT_ROOT"
echo "Remote Path: $REMOTE_PATH"
echo "=================================="

# Test SSH connection over Tailscale SSH
# Note: kept fully interactive so Tailscale re-auth URLs surface to the terminal.
echo "Checking Tailscale SSH connection..."
if ! ssh -o ConnectTimeout=10 "$REMOTE_HOST" exit; then
    echo "Error: Cannot connect to $REMOTE_HOST via SSH."
    echo "Please ensure Tailscale SSH is enabled and authorized on both machines."
    exit 1
fi
echo "SSH Connection OK."

# Perform sync
for dir in "${SYNC_DIRS[@]}"; do
    if [[ "$DIRECTION" == "push" ]]; then
        # Push: local -> remote
        if [[ -d "$dir" ]]; then
            echo "Pushing $dir..."
            # Ensure remote parent directory exists (dirname evaluated on remote shell)
            ssh "$REMOTE_HOST" "mkdir -p \"$(dirname "$REMOTE_PATH/$dir")\""
            rsync -avz --exclude '.git/' --exclude 'README.md' "$dir/" "$REMOTE_HOST:$REMOTE_PATH/$dir/"
        else
            echo "Skipping $dir (local directory does not exist)"
        fi
    else
        # Pull: remote -> local
        # Check if remote directory exists first
        if ssh "$REMOTE_HOST" "[ -d \"$REMOTE_PATH/$dir\" ]"; then
            echo "Pulling $dir..."
            mkdir -p "$(dirname "$dir")"
            rsync -avz --exclude '.git/' --exclude 'README.md' "$REMOTE_HOST:$REMOTE_PATH/$dir/" "$dir/"
        else
            echo "Skipping $dir (remote directory does not exist)"
        fi
    fi
done

echo "Sync completed successfully!"
