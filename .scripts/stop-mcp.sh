#!/usr/bin/env bash

# Calculate the path independent of current working directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PID_FILE="$PROJECT_ROOT/.private/warlock-mcp.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "No PID file found. Verify Warlock MCP Server is running."
    exit 0
fi

PID=$(cat "$PID_FILE")

if kill -0 "$PID" 2>/dev/null; then
    echo "Stopping Warlock MCP Server (PID: $PID)"
    kill "$PID"

    # Grace period
    for i in {1..5}; do
        if ! kill -0 "$PID" 2>/dev/null; then
            break;
        fi
        sleep 1
    done

    if kill -0 "$PID" 2>/dev/null; then
        echo "Process did not stop gracefully. Sending SIGKILL..."
        kill -9 "$PID"
    fi
    echo "Warlock MCP Server stopped"
else
    echo "Process ID ($PID) is not running. Cleaning up stale PID file."
fi

rm -f "$PID_FILE"
