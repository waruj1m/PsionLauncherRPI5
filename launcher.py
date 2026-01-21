#!/usr/bin/env python3
"""
Psion-inspired Launcher for Raspberry Pi
A retro grid-based application launcher using Tkinter
"""

import sys
import json
import subprocess
import re
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import psutil
import threading
import time


class StatusBar(tk.Frame):
    """Status bar showing system metrics"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#1E1E1E', height=36)
        self.pack_propagate(False)
        
        # Container for metrics
        metrics_frame = tk.Frame(self, bg='#2C2C2C')
        metrics_frame.pack(side=tk.RIGHT, padx=10)
        
        # Create metric labels
        self.cpu_label = self.create_metric_label(metrics_frame, "CPU: --")
        self.ram_label = self.create_metric_label(metrics_frame, "RAM: --")
        self.disk_label = self.create_metric_label(metrics_frame, "SSD: --")
        self.net_label = self.create_metric_label(metrics_frame, "NET: --")
        self.wifi_label = self.create_metric_label(metrics_frame, "WiFi: --")
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_metrics, daemon=True)
        self.update_thread.start()
    
    def create_metric_label(self, parent, text):
        """Create a styled metric label"""
        label = tk.Label(
            parent,
            text=text,
            font=('Monospace', 9),
            bg='#1E1E1E',
            fg='#FFFFFF',
            relief=tk.FLAT,
            padx=8
        )
        label.pack(side=tk.LEFT)
        return label
    
    def update_metrics(self):
        """Update system metrics periodically"""
        last_net_io = psutil.net_io_counters(pernic=True).get('wlan0', psutil.net_io_counters())
        last_time = time.time()
        
        while self.running:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.5)
                self.cpu_label.config(text=f"CPU: {cpu_percent:.0f}%")
                
                # RAM usage
                ram = psutil.virtual_memory()
                self.ram_label.config(text=f"RAM: {ram.percent:.0f}%")
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.disk_label.config(text=f"SSD: {disk.percent:.0f}%")
                
                # Network speed
                current_net_io = psutil.net_io_counters(pernic=True).get('wlan0', psutil.net_io_counters())
                current_time = time.time()
                time_delta = current_time - last_time
                
                if time_delta > 0:
                    bytes_sent = current_net_io.bytes_sent - last_net_io.bytes_sent
                    bytes_recv = current_net_io.bytes_recv - last_net_io.bytes_recv
                    
                    # Calculate speed in KB/s
                    upload_speed = (bytes_sent / time_delta) / 1024
                    download_speed = (bytes_recv / time_delta) / 1024
                    
                    # Format based on magnitude
                    if download_speed > 1024:
                        net_text = f"NET: ↓{download_speed/1024:.1f}MB/s"
                    elif download_speed > 1:
                        net_text = f"NET: ↓{download_speed:.0f}KB/s"
                    else:
                        net_text = "NET: --"
                    
                    self.net_label.config(text=net_text)
                
                # WiFi status
                try:
                    wifi_info = subprocess.run(
                        "iwconfig wlan0 2>/dev/null | grep 'Link Quality'",
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=1
                    )
                    if wifi_info.returncode == 0 and wifi_info.stdout:
                        # Extract signal quality
                        quality_match = re.search(r'Link Quality=(\d+)/(\d+)', wifi_info.stdout)
                        if quality_match:
                            quality = int(quality_match.group(1))
                            max_quality = int(quality_match.group(2))
                            percent = int((quality / max_quality) * 100)
                            self.wifi_label.config(text=f"WiFi: {percent}%")
                        else:
                            self.wifi_label.config(text="WiFi: --")
                    else:
                        self.wifi_label.config(text="WiFi: 0%")
                except:
                    self.wifi_label.config(text="WiFi: 0%")
                
                last_net_io = current_net_io
                last_time = current_time
                
                time.sleep(2)  # Update every 2 seconds
                
            except Exception as e:
                print(f"Error updating metrics: {e}")
                time.sleep(2)
    
    def stop(self):
        """Stop the update thread"""
        self.running = False


class SystemInfoWindow:
    """System information window in Psion style"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("System Information")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#F5F5F5')
        
        # Title bar frame
        title_frame = tk.Frame(self.window, bg='#4A90E2', height=30)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="System Information",
            font=('Monospace', 12, 'bold'),
            bg='#4A90E2',
            fg='white',
            anchor='w',
            padx=10
        )
        title_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Button(
            title_frame,
            text="×",
            font=('Monospace', 16, 'bold'),
            bg='#4A90E2',
            fg='white',
            bd=0,
            command=self.window.destroy,
            width=3,
            activebackground='#E74C3C',
            activeforeground='white'
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Info frame with border
        info_frame = tk.Frame(
            self.window,
            bg='white',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text widget for system info
        self.text = tk.Text(
            info_frame,
            font=('Monospace', 10),
            bg='white',
            fg='#000000',
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Load system info
        self.load_system_info()
        
        # Make text read-only
        self.text.configure(state=tk.DISABLED)
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
    
    def load_system_info(self):
        """Load and display system information"""
        self.text.configure(state=tk.NORMAL)
        
        # Try to get system info from various sources
        info_commands = [
            ("OS", "lsb_release -d 2>/dev/null | cut -f2"),
            ("Kernel", "uname -r"),
            ("Hostname", "hostname"),
            ("Uptime", "uptime -p"),
            ("CPU", "lscpu | grep 'Model name' | cut -d':' -f2 | xargs"),
            ("Memory", "free -h | awk '/^Mem:/ {print $2}'"),
            ("Disk", "df -h / | awk 'NR==2 {print $2}'"),
            ("User", "whoami"),
            ("Shell", "echo $SHELL"),
        ]
        
        for label, command in info_commands:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                value = result.stdout.strip() or "N/A"
                self.text.insert(tk.END, f"{label:12s}: {value}\n")
            except Exception as e:
                self.text.insert(tk.END, f"{label:12s}: N/A\n")
        
        # Add separator
        self.text.insert(tk.END, "\n" + "─" * 60 + "\n\n")
        
        # Try to get network info
        try:
            result = subprocess.run(
                "ip -4 addr show | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=2
            )
            ips = result.stdout.strip().split('\n')
            self.text.insert(tk.END, "IP Addresses:\n")
            for ip in ips:
                if ip:
                    self.text.insert(tk.END, f"  • {ip}\n")
        except:
            pass
        
        self.text.configure(state=tk.DISABLED)


class LauncherButton(tk.Frame):
    """Custom button widget for launcher items"""
    
    def __init__(self, parent, app_data, wide=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.app_data = app_data
        self.wide = wide
        self.parent_root = parent.winfo_toplevel()
        
        # Configure frame
        width = 260 if wide else 200
        height = 110 if wide else 160
        
        self.configure(
            bg='#F5F5F5',
            relief=tk.RAISED,
            borderwidth=3,
            highlightthickness=2,
            highlightbackground='#A0A0A0',
            width=width,
            height=height
        )
        self.pack_propagate(False)
        
        if wide:
            # Wide button layout (horizontal)
            content_frame = tk.Frame(self, bg='#F5F5F5')
            content_frame.pack(expand=True)
            
            # Icon on left
            self.icon_label = tk.Label(content_frame, bg='#F5F5F5')
            self.icon_label.pack(side=tk.LEFT, padx=(10, 5))
            
            # Text on right
            self.text_label = tk.Label(
                content_frame,
                text=app_data['name'],
                font=('Monospace', 11, 'bold'),
                bg='#F5F5F5',
                fg='#000000'
            )
            self.text_label.pack(side=tk.LEFT, padx=(5, 10))
        else:
            # Square button layout (vertical)
            self.icon_label = tk.Label(self, bg='#F5F5F5')
            self.icon_label.pack(pady=(10, 5))
            
            self.text_label = tk.Label(
                self,
                text=app_data['name'],
                font=('Monospace', 11, 'bold'),
                bg='#F5F5F5',
                fg='#000000',
                wraplength=160
            )
            self.text_label.pack()
        
        self.load_icon()
        
        # Bind click events
        self.bind('<Button-1>', self.on_click)
        self.icon_label.bind('<Button-1>', self.on_click)
        self.text_label.bind('<Button-1>', self.on_click)
        
        # Bind hover events
        for widget in [self, self.icon_label, self.text_label]:
            widget.bind('<Enter>', self.on_enter)
            widget.bind('<Leave>', self.on_leave)
    
    def load_icon(self):
        """Load or generate icon for the application"""
        icon_path = self.app_data.get('icon', '')
        icon_size = (80, 80) if not self.wide else (70, 70)
        
        try:
            if icon_path and Path(icon_path).exists():
                img = Image.open(icon_path)
                img = img.resize(icon_size, Image.LANCZOS)
            else:
                # Create colored icon with letter
                img = Image.new('RGB', icon_size, self.app_data.get('color', '#4A90E2'))
                draw = ImageDraw.Draw(img)
                
                # Try to use a font, fallback to default
                try:
                    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 32)
                except:
                    font = ImageFont.load_default()
                
                # Draw letter
                letter = self.app_data['name'][0].upper()
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                position = ((icon_size[0] - text_width) // 2, (icon_size[1] - text_height) // 2 - 5)
                draw.text(position, letter, fill='white', font=font)
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(img)
            self.icon_label.configure(image=self.photo)
            
        except Exception as e:
            print(f"Error loading icon for {self.app_data['name']}: {e}")
    
    def on_enter(self, event):
        """Handle mouse enter"""
        self.configure(bg='#E0E0E0')
        self.icon_label.configure(bg='#E0E0E0')
        self.text_label.configure(bg='#E0E0E0')
    
    def on_leave(self, event):
        """Handle mouse leave"""
        self.configure(bg='#F5F5F5')
        self.icon_label.configure(bg='#F5F5F5')
        self.text_label.configure(bg='#F5F5F5')
    
    def on_click(self, event):
        """Handle click event"""
        # Visual feedback
        self.configure(bg='#C0C0C0')
        self.icon_label.configure(bg='#C0C0C0')
        self.text_label.configure(bg='#C0C0C0')
        self.after(100, lambda: self.on_leave(None))
        
        # Launch app
        self.launch_app()
    
    def launch_app(self):
        """Launch the application"""
        app_type = self.app_data.get('type', 'exec')
        
        try:
            if app_type == 'exec':
                command = self.app_data['command']
                # If command is a script ending in .sh, launch in new terminal
                if command.endswith('.sh'):
                    # Launch in new terminal window
                    subprocess.Popen(['x-terminal-emulator', '-e', command])
                else:
                    subprocess.Popen(command, shell=True)
            elif app_type == 'url':
                subprocess.Popen(['xdg-open', self.app_data['command']])
            elif app_type == 'system':
                self.handle_system_command()
            elif app_type == 'system_info':
                self.show_system_info()
            elif app_type == 'exit':
                self.parent_root.quit()
                self.parent_root.destroy()
        except Exception as e:
            messagebox.showerror("Launch Error", 
                               f"Failed to launch {self.app_data['name']}:\n{str(e)}")
    
    def handle_system_command(self):
        """Handle system commands like shutdown/restart"""
        result = messagebox.askyesno(
            "Confirm",
            f"Are you sure you want to {self.app_data['name']}?"
        )
        if result:
            subprocess.Popen(self.app_data['command'], shell=True)
    
    def show_system_info(self):
        """Show system information window"""
        SystemInfoWindow(self.parent_root)


class PsionLauncher:
    """Main launcher application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.config_path = Path(__file__).parent / 'config.json'
        self.load_config()
        self.init_ui()
    
    def load_config(self):
        """Load configuration from JSON file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Save configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "display": {
                "width": 1560,
                "height": 720,
                "title": "Psion Launcher"
            },
            "grid": {
                "columns": 3,
                "rows": 2
            },
            "theme": {
                "background": "#B0B0B0",
                "text": "#000000"
            },
            "applications": [
                {
                    "name": "Warp",
                    "type": "exec",
                    "command": "warp-terminal",
                    "icon": "warp.png",
                    "color": "#2ECC71"
                },
                {
                    "name": "Firefox",
                    "type": "exec",
                    "command": "firefox",
                    "icon": "firefox.png",
                    "color": "#E74C3C"
                },
                {
                    "name": "VS Code",
                    "type": "exec",
                    "command": "code",
                    "icon": "vscode.png",
                    "color": "#3498DB"
                },
                {
                    "name": "ChatGPT",
                    "type": "url",
                    "command": "https://chat.openai.com",
                    "icon": "chatgpt.png",
                    "color": "#10A37F"
                },
                {
                    "name": "File Manager",
                    "type": "exec",
                    "command": "pcmanfm",
                    "icon": "filemanager.png",
                    "color": "#F39C12"
                }
            ],
            "side_buttons": [
                {
                    "name": "Settings",
                    "type": "exec",
                    "command": "lxappearance",
                    "icon": "settings.png",
                    "color": "#9B59B6"
                },
                {
                    "name": "System",
                    "type": "system_info",
                    "icon": "systemWide.png",
                    "color": "#34495E"
                },
                {
                    "name": "Restart",
                    "type": "system",
                    "command": "sudo reboot",
                    "icon": "restartWide.png",
                    "color": "#E67E22"
                },
                {
                    "name": "Shutdown",
                    "type": "system",
                    "command": "sudo shutdown -h now",
                    "icon": "powerWide.png",
                    "color": "#C0392B"
                }
            ]
        }
    
    def init_ui(self):
        """Initialize the user interface"""
        # Configure window
        self.root.title(self.config['display']['title'])
        self.root.geometry(f"{self.config['display']['width']}x{self.config['display']['height']}")
        self.root.attributes("-fullscreen", True)
        self.root.configure(cursor="arrow")
        self.root.resizable(False, False)
        self.root.configure(bg=self.config['theme']['background'])
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.on_close())
        self.root.bind('q', lambda e: self.on_close())
        self.root.bind('Q', lambda e: self.on_close())
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Status bar at top
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.TOP)
        
        # Title
        title = tk.Label(
            self.root,
            text=self.config['display']['title'],
            font=('Monospace', 24, 'bold'),
            bg=self.config['theme']['background'],
            fg=self.config['theme']['text'],
            pady=10
        )
        title.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.config['theme']['background'])
        content_frame.pack(expand=True, pady=20)
        
        # Left side: Grid of main application buttons
        grid_frame = tk.Frame(content_frame, bg=self.config['theme']['background'])
        grid_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        apps = self.config['applications']
        cols = self.config['grid']['columns']
        
        for i, app in enumerate(apps):
            row = i // cols
            col = i % cols
            
            btn = LauncherButton(grid_frame, app)
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        # Right side: Vertical stack of wide buttons
        side_frame = tk.Frame(content_frame, bg=self.config['theme']['background'])
        side_frame.pack(side=tk.LEFT)
        
        side_buttons = self.config.get('side_buttons', [])
        for side_btn_data in side_buttons:
            btn = LauncherButton(side_frame, side_btn_data, wide=True)
            btn.pack(pady=10)
    
    def on_close(self):
        """Handle application close"""
        self.status_bar.stop()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    try:
        launcher = PsionLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
