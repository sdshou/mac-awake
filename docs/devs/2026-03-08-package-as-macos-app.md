# Dev Summary: Package mac-awake as a macOS .app

**Date:** 2026-03-08
**Feature:** Standalone macOS app bundle

## What Changed

Packaged mac-awake as a standalone `.app` bundle using py2app, so users can launch it by double-clicking in Finder instead of running `python app.py` from the terminal.

## Files Added

| File | Purpose |
|------|---------|
| `setup.py` | py2app build configuration |
| `create_icon.py` | Helper script to generate `icon.icns` from Pillow drawings |
| `icon.icns` | Coffee cup app icon (generated) |
| `.gitignore` | Ignore `build/`, `dist/`, and other artifacts |

## Files Modified

| File | Change |
|------|--------|
| `requirements.txt` | Added `py2app` |
| `README.md` | Added "Build as macOS App" section |

## Key Decisions

- **py2app over PyInstaller**: py2app is macOS-native and handles `.app` bundle conventions (Info.plist, LSUIElement, iconset) more naturally.
- **LSUIElement: True**: The app is menu-bar-only — no dock icon, no main window.
- **Bundle ID**: `com.sdshou.mac-awake`
- **Icon generation via Pillow**: A Python script (`create_icon.py`) draws a coffee cup programmatically, exports to `.iconset` PNGs, then uses macOS `iconutil` to produce `icon.icns`. This avoids needing external design tools.

## How to Build

```bash
pip install -r requirements.txt
python setup.py py2app
open "dist/Mac Awake.app"
```

## Verification Done

- Build completes without errors
- App launches and shows ☕/💤 menu bar icon
- No dock icon appears
- Process runs correctly (confirmed via `pgrep`)
- Info.plist contains correct bundle name, identifier, icon path, and `LSUIElement: true`
