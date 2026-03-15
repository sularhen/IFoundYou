#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

USER_BIN="${HOME}/.local/bin"

echo "Installing IFoundYou from local release package..."
python3 -m pip install --user .
mkdir -p "$USER_BIN"
cp "$SCRIPT_DIR/ifoundyou" "$USER_BIN/ifoundyou"
chmod +x "$USER_BIN/ifoundyou"
echo
echo "Installed. Main command:"
echo "  ifoundyou github.com"
echo
echo "If your shell does not find it yet, add this to your PATH:"
echo "  export PATH=\"$USER_BIN:\$PATH\""
