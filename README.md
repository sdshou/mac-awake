# mac-awake

A tiny macOS menu bar app that prevents your MacBook from sleeping.

## Requirements

- macOS (any modern version)
- Python 3.8+

## Install & Run

```bash
cd mac-awake
pip install -r requirements.txt
python app.py
```

A ☕ / 💤 icon appears in your menu bar.

## Build as macOS App

Package mac-awake as a standalone `.app` bundle you can double-click from Finder:

```bash
pip install -r requirements.txt
python setup.py py2app
open "dist/Mac Awake.app"
```

The built app is at `dist/Mac Awake.app`. Drag it to your Applications folder to install.

## Usage

| Action | How |
|--------|-----|
| Toggle awake on/off | Click the menu bar icon → **Keep Awake** |
| Set a timer | Click **Set Timer** and pick a duration |
| Check elapsed time | The status line updates every 5 seconds |
| Quit | Click **Quit** |

## How it works

Spawns macOS's built-in `caffeinate -di` to block both **display sleep** and
**idle system sleep**. When the optional timer expires the process is killed
and a notification fires. No root privileges, no kext — just one subprocess.

## Quit cleanly

Use **Quit** from the menu — this terminates `caffeinate` before exiting so
your normal sleep settings are immediately restored.
