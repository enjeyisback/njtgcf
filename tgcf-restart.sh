#!/bin/bash
# TGCF Restart Script
# This script restarts the TGCF service

set -e

echo "Restarting TGCF service..."
echo ""

# Stop the service if running
./tgcf-stop.sh

# Wait a moment
sleep 2

# Start the service
./tgcf-start.sh

echo ""
echo "TGCF service restarted successfully!"
