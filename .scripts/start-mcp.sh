#!/usr/bin/env bash

# Calculate the path independent of current working directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PID_FILE="$PROJECT_ROOT/.private/warlock-mcp.pid"
LOG_FILE="$PROJECT_ROOT/.private/logs/warlock-mcp.log"

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Warlock MCP Server is already running (PID: $PID)"
        exit 0
    else
        # PID file is stale
        rm -f "$PID_FILE"
    fi
fi

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Locate UV
UV_BIN="uv"
if ! command -v uv &>/dev/null; then
    if [ -f "$HOME/.local/bin/uv" ]; then
        UV_BIN="$HOME/.local/bin/uv"
    elif [ -f "/usr/local/bin/uv" ]; then
        UV_BIN="/usr/local/bin/uv"
    else
        echo "Error: 'uv' not found in PATH or standard user directories ($HOME/.local/bin/uv)." >&2
        exit 1
    fi
fi

echo "Starting Warlock MCP Server headlessly using UV..."
echo "Logs: $LOG_FILE"

cd "$PROJECT_ROOT" || exit

# Start Warlock MCP Server headlessly with UV and nohup
nohup "$UV_BIN" run python -m warlock.main --log-file "$LOG_FILE" --transport streamable-http "$@" < /dev/null > "$PROJECT_ROOT/.private/logs/stdout.log" 2>&1 &

NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"
echo "Warlock MCP Server started successfully (PID: $NEW_PID)."
