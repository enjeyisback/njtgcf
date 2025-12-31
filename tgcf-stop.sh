#!/bin/bash
# TGCF Stop Script
# This script stops the TGCF service running in tmux

set -e

TMUX_SESSION="tgcf-service"

# Check if session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "TGCF service is not running (no tmux session found: $TMUX_SESSION)"
    exit 0
fi

# Stop the tmux session
echo "Stopping TGCF service (tmux session: $TMUX_SESSION)..."
tmux kill-session -t "$TMUX_SESSION"

echo "TGCF service stopped successfully!"
