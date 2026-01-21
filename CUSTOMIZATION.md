# Customization Guide

## Quick Reference

### Configuration File Location
`config.json` (created automatically on first run)

### Display Settings

```json
"display": {
  "width": 1560,
  "height": 720,
  "title": "Psion Launcher"
}
```

### Grid Layout

```json
"grid": {
  "columns": 4,
  "rows": 2
}
```

Adjust these to fit more/fewer apps on screen.

### Theme Colors

```json
"theme": {
  "background": "#C0C0C0",
  "text": "#000000"
}
```

Use hex color codes. Examples:
- Classic gray: `#C0C0C0`
- Psion green: `#A8B090`
- Dark mode: `#2C3E50`

### Application Entry Format

```json
{
  "name": "Display Name",
  "type": "exec|url|system",
  "command": "command-or-url",
  "color": "#HEX_COLOR",
  "icon": "/optional/path/to/icon.png"
}
```

### Application Types

**exec** - Run a program:
```json
{
  "name": "Terminal",
  "type": "exec",
  "command": "gnome-terminal",
  "color": "#2ECC71"
}
```

**url** - Open a website:
```json
{
  "name": "GitHub",
  "type": "url",
  "command": "https://github.com",
  "color": "#333333"
}
```

**system** - System command (shows confirmation):
```json
{
  "name": "Shutdown",
  "type": "system",
  "command": "sudo shutdown -h now",
  "color": "#C0392B"
}
```

### Common Application Commands

- **Terminals**: `gnome-terminal`, `xterm`, `konsole`, `warp-terminal`
- **Browsers**: `firefox`, `chromium-browser`, `google-chrome`
- **Editors**: `code` (VS Code), `gedit`, `nano`, `vim`
- **File Managers**: `pcmanfm`, `nautilus`, `dolphin`, `thunar`
- **System**: `lxappearance` (settings), `htop` (system monitor)

### Color Palette Ideas

**Retro Computing:**
- Psion Green: `#A8B090`
- Amber: `#FFBF00`
- Green CRT: `#33FF33`

**Modern:**
- Material Blue: `#2196F3`
- Material Red: `#F44336`
- Material Green: `#4CAF50`

**Vibrant:**
- Purple: `#9B59B6`
- Orange: `#E67E22`
- Turquoise: `#1ABC9C`

### Tips

1. **Test commands first**: Run commands in terminal before adding to launcher
2. **Icon sizes**: Icons work best at 64x64 or 128x128 pixels
3. **Button spacing**: Adjust grid spacing in code if buttons overlap
4. **Backup config**: Copy `config.json` before making major changes
5. **Theme files**: Place theme JSONs in `themes/` directory for future use

### Finding Application Commands

```bash
# Find installed applications
ls /usr/bin | grep -i <app_name>

# Check if command exists
which firefox
which code

# List desktop applications
ls /usr/share/applications
```

### Future: Full Theme Support

Theme files in `themes/` directory are ready for when theme switching is implemented.
Each theme can define:
- Background color
- Text color  
- Button colors (normal, hover, pressed)
- Border colors

Stay tuned for theme selector feature!
