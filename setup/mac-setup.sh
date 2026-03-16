#!/bin/bash
# The Builder's Bible — Mac Setup Script
# Run this to set up your development environment on macOS

set -e

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║   The Builder's Bible — Mac Setup    ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# Check for Xcode Command Line Tools (includes Git)
echo "  [1/5] Checking for Git..."
if ! command -v git &> /dev/null; then
    echo "        Installing Xcode Command Line Tools (includes Git)..."
    xcode-select --install
    echo "        Please complete the installation dialog, then re-run this script."
    exit 1
else
    echo "        ✓ Git $(git --version | cut -d' ' -f3)"
fi

# Check for Node.js
echo "  [2/5] Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo "        Node.js not found. Installing via official installer..."
    echo "        Please download and install from: https://nodejs.org (LTS version)"
    echo "        Then re-run this script."
    open "https://nodejs.org"
    exit 1
else
    echo "        ✓ Node.js $(node --version)"
    echo "        ✓ npm $(npm --version)"
fi

# Check for VS Code
echo "  [3/5] Checking for VS Code..."
if ! command -v code &> /dev/null; then
    echo "        VS Code not found."
    echo "        Download from: https://code.visualstudio.com"
    echo "        (This is optional — you can use any code editor)"
else
    echo "        ✓ VS Code installed"
fi

# Install Claude Code
echo "  [4/5] Checking for Claude Code..."
if ! command -v claude &> /dev/null; then
    echo "        Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code
    echo "        ✓ Claude Code installed"
    echo "        Note: You'll need a Claude Pro account ($20/mo) to use it."
    echo "        Sign up at: https://claude.ai"
else
    echo "        ✓ Claude Code installed"
fi

# Create exercises directory
echo "  [5/5] Setting up exercises directory..."
EXERCISES_DIR="$HOME/Desktop/builders-bible-exercises"
if [ ! -d "$EXERCISES_DIR" ]; then
    mkdir -p "$EXERCISES_DIR"
    echo "I started The Builder's Bible on $(date)" > "$EXERCISES_DIR/started.txt"
    echo "        ✓ Created $EXERCISES_DIR"
else
    echo "        ✓ $EXERCISES_DIR already exists"
fi

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║         Setup Complete! 🎉           ║"
echo "  ╠══════════════════════════════════════╣"
echo "  ║  Your tools:                         ║"
echo "  ║  • Git ✓                             ║"
echo "  ║  • Node.js ✓                         ║"
echo "  ║  • npm ✓                             ║"
echo "  ║  • Claude Code ✓                     ║"
echo "  ║                                      ║"
echo "  ║  Next: Open the book and start       ║"
echo "  ║  with Part 0, Chapter 0.1            ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
