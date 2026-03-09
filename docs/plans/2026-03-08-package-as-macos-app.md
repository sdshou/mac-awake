# Plan: Package mac-awake as a macOS .app

**Date:** 2026-03-08
**Status:** Completed

## Goal

Package mac-awake as a standalone macOS `.app` bundle that can be launched by double-clicking in Finder, with a custom icon. Currently the app requires running `python app.py` from the terminal.

## Approach: py2app

Use `py2app` to bundle the Python script + rumps dependency into a standalone `.app`.

## Files to Create / Modify

### New Files

1. **`setup.py`** — py2app build configuration
   - `LSUIElement: True` (menu bar only, no dock icon)
   - Bundle name: "Mac Awake"
   - Bundle identifier: `com.sdshou.mac-awake`
   - Reference the generated icon file

2. **`icon.icns`** — App icon (coffee cup)
   - Generate a coffee cup icon using Python (Pillow) → PNG → `.icns`
   - Use macOS `iconutil` to convert from `.iconset` to `.icns`
   - Helper script: `create_icon.py`

3. **`.gitignore`** — Ignore build artifacts
   - `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.claude/`, `.mcp.json*`

### Modified Files

4. **`requirements.txt`** — Add `py2app` as a build dependency
5. **`README.md`** — Add build instructions section

## Build & Run

```bash
pip install -r requirements.txt
python setup.py py2app
open "dist/Mac Awake.app"
```

The built app will be at `dist/Mac Awake.app`.

## Verification Criteria

1. `python setup.py py2app` builds without errors
2. `dist/Mac Awake.app` launches and shows menu bar icon
3. App icon (coffee cup) shows in Finder
4. No dock icon appears (`LSUIElement: True`)
5. Toggle, timer, and quit functionality all work

## Alternatives Considered

- **PyInstaller**: More general-purpose, but py2app is macOS-native and integrates better with `.app` bundle conventions (Info.plist, iconset, LSUIElement).
- **Nuitka**: Compiles to native code for better performance, but adds complexity and longer build times for a simple menu bar app.
- **Manual .app bundle**: Creating the bundle structure by hand is fragile and harder to maintain.
