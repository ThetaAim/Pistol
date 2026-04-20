import os
import subprocess
import tkinter as tk


def check_file_exists(pkg_path):
    """Check if the given file path exists."""
    return os.path.isfile(pkg_path)


def install_pkgs(pkgs, text_widget, event):
    """Install the specified packages using AppleScript with proper quoting."""
    applescript_commands = ''
    log_file = "/tmp/Pistol_log.txt"
    success = False
    # Clear previous log
    # open(log_file, 'w').close()

    for pkg_path, file_name in pkgs:
        if not check_file_exists(pkg_path):
            text_widget.insert(tk.END, f"[!] Package '{file_name}' path not found: {pkg_path}\n")
            continue

        # Escape any double quotes in the path
        escaped_path = pkg_path.replace('"', '\\"')
        escaped_log = log_file.replace('"', '\\"')

        text_widget.insert(tk.END, f"[•] Preparing to install: {file_name}\n")

        # Build AppleScript for this pkg
        applescript_commands += (
            f'do shell script "installer -verbose -pkg \\"{escaped_path}\\" '
            f'-target / >> \\"{escaped_log}\\" 2>&1" with administrator privileges\n'
        )

    if not applescript_commands:
        text_widget.insert(tk.END, "\n[!] No valid packages to install.\n")
        event.set()
        return False

    text_widget.insert(tk.END, f"\n[✓] All packages prepared.\n")
    text_widget.insert(tk.END, "[🔐] Waiting for authentication...\n")
    text_widget.insert(tk.END, "[⌛] This may take up to 10 minutes...\n\n")

    # Run the combined AppleScript
    result = subprocess.run(['osascript', '-e', applescript_commands]).returncode

    if result == 0:
        text_widget.insert(tk.END, f"[✔] All packages installed successfully.\n")
        success = True
    else:
        text_widget.insert(tk.END, f"[✗] Installation failed.\n")
        text_widget.insert(tk.END, f"[📄] Reading log output from {log_file}:\n\n")

        try:
            with open(log_file) as f:
                last_lines = f.readlines()[-20:]
                text_widget.insert(tk.END, ''.join(last_lines))
        except Exception as e:
            text_widget.insert(tk.END, f"[!] Failed to read log: {str(e)}\n")

    event.set()
    return success
