#!/usr/bin/env bash

# Calculate path independent of current working directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ENV_FILE="$PROJECT_ROOT/.private/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment configuration file not found at $ENV_FILE" >&2
    exit 1
fi

set -a
# shellcheck source=/dev/null
source "$ENV_FILE"
set +a

MISSING_VARS=()
[ -z "$MCP_DEPLOY_HOST" ] && MISSING_VARS+=("MCP_DEPLOY_HOST")
[ -z "$MCP_DEPLOY_USER" ] && MISSING_VARS+=("MCP_DEPLOY_USER")
[ -z "$MCP_DEPLOY_DIR" ] && MISSING_VARS+=("MCP_DEPLOY_DIR")

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "Error: Missing required deployment variables in $ENV_FILE:" >&2
    for var in "${MISSING_VARS[@]}"; do
        echo " - $var" >&2
    done
    exit 1
fi

echo "🚀 Deploying to remote MCP host ($MCP_DEPLOY_HOST)..."

ssh -o ConnectTimeout=5 "${MCP_DEPLOY_USER}@${MCP_DEPLOY_HOST}" "cd ${MCP_DEPLOY_DIR} && git pull origin main && .scripts/stop-mcp.sh && .scripts/start-mcp.sh"

echo "✅ Deploy completed successfully."
