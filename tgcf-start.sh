#!/bin/bash
# TGCF Start Script
# This script starts TGCF in a detached tmux session

set -e

# Dynamically detect the project directory (where this script is located)
TGCF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMUX_SESSION="tgcf-service"
LOG_FILE="$TGCF_DIR/tgcf-service.log"

cd "$TGCF_DIR"

# Check if session already exists
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "TGCF service is already running in tmux session: $TMUX_SESSION"
    echo "Use 'tgcf-status.sh' to check status or 'tgcf-stop.sh' to stop it first."
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Start TGCF in a new tmux session
echo "Starting TGCF service in tmux session: $TMUX_SESSION"
tmux new-session -d -s "$TMUX_SESSION" -c "$TGCF_DIR" "tgcf-web 2>&1 | tee -a $LOG_FILE"

echo "TGCF service started successfully!"
echo "Session: $TMUX_SESSION"
echo "Log file: $LOG_FILE"
echo ""
echo "Management commands:"
echo "  - View logs: tail -f $LOG_FILE"
echo "  - Attach to session: tmux attach -t $TMUX_SESSION"
echo "  - Check status: ./tgcf-status.sh"
echo "  - Stop service: ./tgcf-stop.sh"
