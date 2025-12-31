#!/bin/bash
# TGCF Auto-Start Configuration Script
# This script sets up TGCF to start automatically on system boot/login

TGCF_DIR="/home/ubuntu/github_repos/tgcf"
BASHRC="$HOME/.bashrc"
AUTOSTART_LINE="[ -f \"$TGCF_DIR/tgcf-start.sh\" ] && cd \"$TGCF_DIR\" && ./tgcf-start.sh > /dev/null 2>&1 &"

echo "========================================="
echo "TGCF Auto-Start Configuration"
echo "========================================="
echo ""

# Check if auto-start is already configured
if grep -q "tgcf-start.sh" "$BASHRC" 2>/dev/null; then
    echo "Status: Auto-start is already configured in $BASHRC"
    echo ""
    echo "To disable auto-start, edit $BASHRC and remove the line:"
    echo "  $AUTOSTART_LINE"
    exit 0
fi

echo "This will configure TGCF to start automatically when you log in."
echo ""
read -p "Do you want to enable auto-start? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "" >> "$BASHRC"
    echo "# TGCF Auto-Start" >> "$BASHRC"
    echo "$AUTOSTART_LINE" >> "$BASHRC"
    echo ""
    echo "✅ Auto-start enabled successfully!"
    echo ""
    echo "TGCF will now start automatically on your next login."
    echo ""
    echo "To disable auto-start, edit $BASHRC and remove the line:"
    echo "  $AUTOSTART_LINE"
else
    echo "Auto-start configuration cancelled."
fi

echo ""
echo "========================================="
