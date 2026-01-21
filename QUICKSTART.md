# Quick Start Guide

## Launch the Launcher

```bash
./launch.sh
```

That's it! The launcher will appear in a 1560x720 window.

## Controls

- **Click** any button to launch that app
- **Press ESC or Q** to quit the launcher
- **Hover** over buttons for highlight effect

## First Time Setup

The launcher auto-creates `config.json` on first run with these apps:
1. Terminal (Warp)
2. Firefox
3. VS Code
4. ChatGPT (web)
5. File Manager
6. Settings
7. Restart (with confirmation)
8. Shutdown (with confirmation)

## Customize

Edit `config.json` to add/remove apps or change colors.

See `CUSTOMIZATION.md` for detailed info.

## Troubleshooting

**Launcher won't start:**
```bash
./setup.sh  # Check dependencies
```

**VS Code button doesn't work:**
The command might be `code-oss` or something else. Check with:
```bash
which code
```
Then update in `config.json`.

**Wrong display size:**
Edit `config.json` and change the `display` width/height values.

## Tech Stack

- **Python 3.13** with Tkinter (built-in GUI)
- **Pillow** for icon generation
- **JSON** config for easy customization

Enjoy your retro launcher! 🚀
