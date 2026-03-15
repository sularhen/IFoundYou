#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

echo "Installing IFoundYou from local release package..."
python3 -m pip install .
echo
echo "Installed. Run it with:"
echo "  python3 -m ifoundyou github.com"
echo
echo "Optional wrapper:"
echo "  ./whereareyou.sh github.com"
