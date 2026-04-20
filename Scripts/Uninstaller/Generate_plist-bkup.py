import os
import pwd
import shutil
import subprocess
from datetime import datetime


def generate_a_plist(year, month, day, hour, minute):
    username = os.getenv('USER')
    user_home = os.path.expanduser(f"~{username}")
    plist_path = os.path.join(user_home, "Library/LaunchAgents/com.ys.remove.printers.plist")
    executable_path = os.path.join(user_home, "Library/Application Support/Pistol/prim_end.app/Contents/MacOS/main")

    plist_agent = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ys.remove.printers</string>
    <key>ProgramArguments</key>
    <array>
        <string>{executable_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Year</key>
        <integer>{year}</integer>
        <key>Month</key>
        <integer>{month}</integer>
        <key>Day</key>
        <integer>{day}</integer>
        <key>Hour</key>
        <integer>{hour}</integer>
        <key>Minute</key>
        <integer>{minute}</integer>
    </dict>
    <key>LaunchOnlyOnce</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/remove_printers.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/remove_printers.err</string>
</dict>
</plist>
"""

    # Write the plist
    with open(plist_path, "w") as file:
        file.write(plist_agent)

    # Set correct permissions
    os.chmod(plist_path, 0o644)
    uid = pwd.getpwnam(username).pw_uid
    gid = pwd.getpwnam(username).pw_gid
    os.chown(plist_path, uid, gid)

    print(f"✅ Plist created at: {plist_path}")
    load_agent(plist_path, uid)


def load_agent(plist_path, uid):
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", plist_path])
    print("✅ LaunchAgent loaded.")
    # launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.ys.remove.printers.plist


