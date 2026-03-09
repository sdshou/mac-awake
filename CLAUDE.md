# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-file macOS menu bar app (Python + `rumps`) that prevents the Mac from sleeping by spawning `caffeinate -di` as a subprocess. The entire app lives in `app.py`.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app (launches a menu bar icon)
python app.py
```

There are no tests, no linter config, and no build system.

## Architecture

- **`app.py`**: `MacAwakeApp` subclasses `rumps.App` to create the menu bar UI. It manages a `caffeinate` subprocess via `subprocess.Popen` and uses a background `threading.Thread` to tick the elapsed-time status label every 5 seconds.
- **`TIMERS` dict**: Maps display labels to durations in seconds (`None` = indefinite). Changing timer while awake restarts the `caffeinate` process with the new duration.
- **`caffeinate`**: macOS built-in; `-d` prevents display sleep, `-i` prevents idle sleep, `-t N` sets a timeout. The app also manually terminates the process on stop/quit for immediate effect.
- **Dependency**: Only `rumps` (menu bar framework). No Xcode or native extensions needed.
