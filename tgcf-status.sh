#!/bin/bash
# TGCF Status Script
# This script checks the status of the TGCF service

TMUX_SESSION="tgcf-service"
TGCF_DIR="/home/ubuntu/github_repos/tgcf"
LOG_FILE="$TGCF_DIR/tgcf-service.log"

echo "========================================="
echo "TGCF Service Status"
echo "========================================="
echo ""

# Check if tmux session exists
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "Status: ✅ RUNNING"
    echo "Session: $TMUX_SESSION"
    echo ""
    
    # Show tmux session info
    echo "Tmux Session Info:"
    tmux list-sessions | grep "$TMUX_SESSION" || true
    echo ""
    
    # Check for running processes
    echo "Running Processes:"
    ps aux | grep -E "tgcf|streamlit" | grep -v grep | grep -v "tgcf-status" || echo "  No TGCF processes found in ps"
    echo ""
    
    # Show last 10 lines of log
    if [ -f "$LOG_FILE" ]; then
        echo "Recent Logs (last 10 lines):"
        echo "---"
        tail -n 10 "$LOG_FILE"
        echo "---"
        echo ""
        echo "Full log: $LOG_FILE"
    fi
    
    echo ""
    echo "Management Commands:"
    echo "  - View logs: tail -f $LOG_FILE"
    echo "  - Attach to session: tmux attach -t $TMUX_SESSION (Ctrl+B then D to detach)"
    echo "  - Stop service: ./tgcf-stop.sh"
    echo "  - Restart service: ./tgcf-restart.sh"
    
else
    echo "Status: ❌ NOT RUNNING"
    echo "Session: $TMUX_SESSION (not found)"
    echo ""
    echo "To start the service, run: ./tgcf-start.sh"
fi

echo ""
echo "========================================="
