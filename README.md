# Psion Launcher

A retro Psion/SymbianOS-inspired launcher for Raspberry Pi with a modern twist.

## Features

- **Retro Grid Layout**: Classic Psion-style icon grid with labels
- **Full Color Support**: Takes advantage of modern displays
- **Easy Configuration**: JSON-based config for apps and themes
- **Modular Design**: Add/remove apps easily
- **System Functions**: Built-in shutdown/restart buttons
- **Keyboard Support**: Press ESC or Q to quit
- **Lightweight**: Built with Tkinter for maximum compatibility

## Usage

### Running the Launcher

```bash
cd /home/james/Dev/psion-launcher
./launch.sh
```

Or from anywhere:

```bash
python3 /home/james/Dev/psion-launcher/launcher.py
```

### Configuration

Edit `config.json` to customize:

- **Display settings**: Change window size and title
- **Grid layout**: Adjust columns and rows
- **Theme colors**: Modify background and text colors
- **Applications**: Add, remove, or modify launcher items

### Adding New Applications

Add entries to the `applications` array in `config.json`:

```json
{
  "name": "App Name",
  "type": "exec",
  "command": "command-to-run",
  "color": "#HEX_COLOR"
}
```

**Types:**
- `exec`: Launch executable command
- `url`: Open URL in default browser
- `system`: System command (with confirmation dialog)

### Custom Icons

To use custom icons, add an `icon` field with the path to your icon file:

```json
{
  "name": "My App",
  "type": "exec",
  "command": "myapp",
  "icon": "/path/to/icon.png",
  "color": "#4A90E2"
}
```

If no icon is specified, a colored square with the first letter will be generated.

## Display Configuration

The launcher is configured for a 1560x720 display (720x1560 rotated 90°).
To change display settings, edit the `display` section in `config.json`.

## Dependencies

- Python 3 (built-in)
- Tkinter (`python3-tk` - usually built-in)
- Pillow (`python3-pil` - for icon generation)

Run `./setup.sh` to check and install dependencies.

## Future Enhancements

- Theme system for easy visual customization
- Icon pack support
- Touchscreen gestures
- Widget support (clock, system info, etc.)

## Technical Notes

This launcher uses Tkinter instead of PyQt5 for better stability and performance on Raspberry Pi.
The original PyQt5 version is backed up as `launcher.py.backup` if needed.
