import curses
import os
import subprocess
import threading
import platform
import time

def get_bloatware_list():
    bloatware = [
        "3D Viewer",
        "Adobe Express",
        "Clipchamp",
        "Facebook",
        "Hidden City: Hidden Object Adventure",
        "Instagram",
        "Netflix",
        "News",
        "Prime Video",
        "Solitaire Collection",
        "Mixed Reality Portal",
        "Roblox",
        "TikTok",
        "Age of Empires: Castle Siege",
        "Asphalt 8: Airborne",
        "Bubble Witch 3 Saga",
        "Candy Crush Friends Saga",
        "Candy Crush Saga",
        "FarmVille 2: Country Escape",
        "Fitbit Coach",
        "Gardenscapes",
        "Phototastic Collage",
        "PicsArt Photo Studio: Collage Maker and Pic Editor",
        "Print 3D",
        "Spotify",
        "Twitter",
    ]
    return bloatware

def get_os_version():
    version = platform.version()
    if "10" in version:
        return "Windows 10"
    elif "11" in version:
        return "Windows 11"
    else:
        return "Unknown"

def scan_bloatware(stdscr, height):
    version = get_os_version()
    bloatware = get_bloatware_list()
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Scanning for bloatware...", curses.color_pair(4))
    stdscr.refresh()
    
    installed_bloatware = []
    for app in bloatware:
        stdscr.addstr(height - len(bloatware) - 1, 0, f"Scanning for {app}...", curses.color_pair(3))
        stdscr.refresh()
        
        if version == "Windows 10":
            result = subprocess.run(["powershell", "-Command", f"Get-AppxPackage -Name {app}"], capture_output=True, text=True)
        elif version == "Windows 11":
            result = subprocess.run(["powershell", "-Command", f"Get-AppxPackage -Name {app}"], capture_output=True, text=True)
        
        if result.returncode == 0:
            installed_bloatware.append(app)
    
    stdscr.clear()
    return installed_bloatware

def animate_title():
    title = "NoBloat By Germanized"
    while True:
        for i in range(len(title)):
            os.system(f"title {title[:i + 1]}")  # Update the CMD window title
            time.sleep(0.1)
        for i in range(len(title), -1, -1):
            os.system(f"title {title[:i + 1]}")  # Update the CMD window title
            time.sleep(0.1)

def main(stdscr):
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    
    # Resize window to fit content
    min_height = 20
    min_width = 60
    if height < min_height:
        curses.resize_term(min_height, width)
        height, width = min_height, width
    if width < min_width:
        curses.resize_term(height, min_width)
        height, width = height, min_width
    
    # Define colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Title
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlighted text
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Scan progress
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Status messages
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)  # Error messages
    
    # Start the animation in a separate thread for the CMD window title
    animation_thread = threading.Thread(target=animate_title)
    animation_thread.daemon = True
    animation_thread.start()
    
    # Scan for bloatware
    installed_bloatware = scan_bloatware(stdscr, height)
    
    # Initialize selected bloatware list
    selected_bloatware = set()
    cursor_y = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "NoBloat By Germanized", curses.color_pair(1))
        subtitle = f"Detected {get_os_version()}. Select bloatware to remove. Press Enter to deselect, Q to quit."
        stdscr.addstr(2, (width // 2) - (len(subtitle) // 2), subtitle, curses.color_pair(4))

        for i, app in enumerate(installed_bloatware):
            if i == cursor_y:
                stdscr.addstr(i + 4, (width // 2) - (len(app) // 2), f"{'X' if app in selected_bloatware else ' '} {app}", curses.color_pair(2))
            else:
                stdscr.addstr(i + 4, (width // 2) - (len(app) // 2), f"{'X' if app in selected_bloatware else ' '} {app}")
        
        stdscr.refresh()

        key = stdscr.getch()
        
        if key == curses.KEY_DOWN:
            cursor_y = min(cursor_y + 1, len(installed_bloatware) - 1)
        elif key == curses.KEY_UP:
            cursor_y = max(cursor_y - 1, 0)
        elif key == 10:  # Enter key
            app = installed_bloatware[cursor_y]
            if app in selected_bloatware:
                selected_bloatware.remove(app)
            else:
                selected_bloatware.add(app)
        elif key == ord('q') or key == ord('Q'):  # Quit
            break

    # Perform removal of selected bloatware
    for app in selected_bloatware:
        stdscr.addstr(height - len(selected_bloatware) - 1, 0, f"Removing {app}...", curses.color_pair(3))
        stdscr.refresh()
        
        if get_os_version() == "Windows 10":
            subprocess.run(["powershell", "-Command", f"Remove-AppxPackage -Name {app}"], capture_output=True, text=True)
        elif get_os_version() == "Windows 11":
            subprocess.run(["powershell", "-Command", f"Remove-AppxPackage -Name {app}"], capture_output=True, text=True)
        
        stdscr.addstr(height - len(selected_bloatware) - 1, 0, f"{app} has been removed.", curses.color_pair(4))
        stdscr.refresh()
        curses.napms(500)  # Wait for 0.5 seconds

    stdscr.addstr(height - len(selected_bloatware) - 1, 0, "Operation completed. Press any key to exit.", curses.color_pair(5))
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
