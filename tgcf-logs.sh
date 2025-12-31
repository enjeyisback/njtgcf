#!/bin/bash
# TGCF Logs Script
# This script shows the logs of the TGCF service

# Dynamically detect the project directory (where this script is located)
TGCF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$TGCF_DIR/tgcf-service.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found: $LOG_FILE"
    echo "The service may not have been started yet."
    exit 1
fi

# Check for command line argument
case "$1" in
    -f|--follow)
        echo "Following TGCF service logs (Ctrl+C to exit):"
        echo "---"
        tail -f "$LOG_FILE"
        ;;
    -n|--lines)
        if [ -z "$2" ]; then
            echo "Error: --lines requires a number argument"
            exit 1
        fi
        tail -n "$2" "$LOG_FILE"
        ;;
    *)
        echo "TGCF Service Logs (last 50 lines):"
        echo "---"
        tail -n 50 "$LOG_FILE"
        echo "---"
        echo ""
        echo "Options:"
        echo "  -f, --follow       Follow log output in real-time"
        echo "  -n, --lines NUM    Show last NUM lines"
        echo ""
        echo "Full log file: $LOG_FILE"
        ;;
esac
