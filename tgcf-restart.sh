#!/bin/bash
# TGCF Restart Script
# This script restarts the TGCF service

set -e

# Dynamically detect the project directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Restarting TGCF service..."
echo ""

# Stop the service if running
"$SCRIPT_DIR/tgcf-stop.sh"

# Wait a moment
sleep 2

# Start the service
"$SCRIPT_DIR/tgcf-start.sh"

echo ""
echo "TGCF service restarted successfully!"
