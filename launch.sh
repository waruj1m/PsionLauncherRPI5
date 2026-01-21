#!/bin/bash
# Launch script for Psion Launcher

cd "$(dirname "$0")"

# Set display if not already set
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

# Launch the application
python3 launcher.py
