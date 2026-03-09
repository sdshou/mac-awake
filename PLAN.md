# mac-awake — Dev Plan

## Goal
A lightweight macOS menu bar app that prevents the laptop from sleeping on demand.

## Approach
- **UI**: `rumps` — a Python library for building macOS menu bar (statusbar) apps
- **Sleep prevention**: macOS built-in `caffeinate` command, launched as a subprocess
  - `caffeinate -d` keeps the display from sleeping
  - `caffeinate -i` keeps the system from idle sleeping
  - Combined: `caffeinate -di` for full awake mode
- **No Xcode required** — pure Python, runs from terminal

## Features (v1)
1. Menu bar icon — ☕ when awake, 💤 when inactive
2. Toggle "Keep Awake" on/off with a click
3. Timer mode — keep awake for a set duration (30 min / 1 hr / 2 hr / custom)
4. Status display — shows elapsed time kept awake
5. "Start on Login" option (via launchd plist)

## Tech Stack
- Python 3.x
- `rumps` — menu bar framework
- `subprocess` — to spawn/kill `caffeinate`
- `threading` — for the elapsed timer

## File Structure
```
mac-awake/
├── PLAN.md           # this file
├── README.md         # usage instructions
├── requirements.txt  # rumps
└── app.py            # main application
```

## Running
```bash
pip install -r requirements.txt
python app.py
```

## Future (v2)
- Packaged as a .app using `py2app`
- Custom icon asset
- Notification when timer expires
