#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_FILE="$SCRIPT_DIR/Integration.py"

if [[ ! -f "$APP_FILE" ]]; then
  echo "Error: Integration.py not found at $APP_FILE" >&2
  exit 1
fi

# Common Python locations on macOS (system, Homebrew Intel/ARM, python.org installers)
PY_CANDIDATES=(
  "/usr/bin/python3"
  "/opt/homebrew/bin/python3"             # Homebrew (Apple Silicon)
  "/usr/local/bin/python3"                # Homebrew (Intel)
  "/Library/Frameworks/Python.framework/Versions/3.8/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.9/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3"
  "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
)

echo "Searching for a compatible Python with Tkinter..."

for py in "${PY_CANDIDATES[@]}"; do
  if [[ -x "$py" ]]; then
    ver="$($py --version 2>&1 || true)"
    echo "Found: $py ($ver)"
    # Check tkinter availability quickly
    if "$py" - <<'PY'
try:
    import tkinter  # noqa: F401
except Exception as e:
    raise SystemExit(3)
PY
    then
      echo "Using: $py"
      exec "$py" "$APP_FILE"
    else
      echo " - Skipping: Tkinter not available."
    fi
  fi
done

cat >&2 <<'EOF'
No compatible Python interpreter with Tkinter was found.

Suggestions:
1) Try the system Python:
   /usr/bin/python3 \
     "/Users/handemo/期中考/Integration.py"

2) Install python.org 3.8 (good Tkinter support for older macOS):
   - Download: https://www.python.org/downloads/release/python-3810/
   - Then run:
     /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 \
       "/Users/handemo/期中考/Integration.py"

3) If using Homebrew:
   - Apple Silicon: /opt/homebrew/bin/python3
   - Intel:         /usr/local/bin/python3
EOF

exit 2


