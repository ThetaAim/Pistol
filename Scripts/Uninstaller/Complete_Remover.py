import os
import pwd
import subprocess
from datetime import datetime

log_path = "/tmp/usafe.log"
printer_log_path = "/tmp/printer_remover.log"
plist_termination_path = "/tmp/pr_end.sh"
target_date = datetime(2025, 10, 26)


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print(f"[LOG ERROR] {e}")


def run(command, ignore_errors=False):
    try:
        subprocess.run(command, shell=True, check=not ignore_errors)
        log(f"✓ Ran: {command}")
    except subprocess.CalledProcessError as e:
        log(f"✗ Failed: {command} — {e}")


def main():
    if datetime.now() < target_date:
        log("⏸ Execution skipped — target date not reached")
        return
    # time.sleep(20) #20 secs
    log(f"🟢 Script started by user: {os.getlogin()}")

    run("pkill -f '/Applications/SafeQClient'", ignore_errors=True)
    run("pkill -f '/Applications/YSoft SafeQ Client'", ignore_errors=True)

    for path in [
        "/Applications/SafeQClient.app",
        "/Applications/YSoft SafeQ Client.app",
        "/usr/libexec/cups/backend/sqport",
        "/Library/PreferencePanes/ClientPreferences.prefPane",
        "/Library/Application Support/YSoft"
    ]:
        run(f"rm -rf '{path}'", ignore_errors=True)

    for plist in [
        "com.ysoft.service.CUPS",
        "com.ysoft.service.DHCPOption"
    ]:
        run(f"launchctl remove {plist}", ignore_errors=True)
        run(f"rm -f /Library/LaunchDaemons/{plist}.plist", ignore_errors=True)

    try:
        user_id = int(subprocess.check_output("stat -f%u /dev/console", shell=True).decode().strip())
        username = subprocess.check_output(f"id -un {user_id}", shell=True).decode().strip()
        run(f"launchctl asuser {user_id} sudo -u {username} launchctl remove com.ysoft.client.agent",
            ignore_errors=True)
    except Exception as e:
        log(f"✗ Could not determine user info: {e}")

    run("rm -f /Library/LaunchAgents/com.ysoft.client.agent.plist", ignore_errors=True)
    run("pkgutil --forget com.ysoft.safeq.client", ignore_errors=True)

    cups_config = "/etc/cups/cups-files.conf"
    if os.path.exists(cups_config):
        run("launchctl stop org.cups.cupsd", ignore_errors=True)
        run("sed -i '' -e 's/Sandboxing Relaxed//g' /etc/cups/cups-files.conf", ignore_errors=True)
        run("launchctl start org.cups.cupsd", ignore_errors=True)

    files_to_remove = [
        "com.apple.print.add.plist",
        "com.apple.print.custompresets.forprinter.Black.plist",
        "com.apple.print.custompresets.forprinter.Color.plist",
        "com.apple.print.custompresets.forprinter.Fiery.plist",
        "com.apple.print.custompresets.forprinter.Mix.plist",
        "com.apple.print.custompresets.forprinter.Unique.plist",
        "com.apple.print.custompresets.plist"
    ]
    prefs_dir = os.path.expanduser("~/Library/Preferences/")
    for file in files_to_remove:
        file_path = os.path.join(prefs_dir, file)
        try:
            os.remove(file_path)
            log(f"Removed: {file_path}")
        except FileNotFoundError:
            log(f"File not found: {file_path}")
        except Exception as e:
            log(f"Error removing {file_path}: {e}")

    printers_to_remove = ["Black", "Fiery", "Unique", "Color"]
    try:
        with open(printer_log_path, "a") as f:
            for printer in printers_to_remove:
                result = os.system(f'/usr/sbin/lpadmin -x "{printer}"')
                if result == 0:
                    f.write(f"[✓] Removed printer: {printer}\n")
                    log(f"Removed printer: {printer}")
                else:
                    f.write(f"[✗] Failed to remove printer: {printer} (Exit code: {result})\n")
                    log(f"Failed to remove printer: {printer} (Exit code: {result})")
    except Exception as e:
        log(f"[✗] Printer log error: {e}")

    log("→ About to run launchctl remove com.ys.remove.printers")

    username = os.getenv("USER")
    uid = pwd.getpwnam(username).pw_uid
    gid = pwd.getpwnam(username).pw_gid

    plist_termination_script = f"""
#!/bin/bash

exec > /dev/null 2>&1
set +x

launchctl remove com.ys.remove.printers

rm -f "$HOME/Library/LaunchAgents/com.ys.remove.printers.plist"
rm -rf "$HOME/Library/Application Support/Pistol/prim_end.app"
rm -f "/private/tmp/Pistol_log.txt"
rm -f "/tmp/usafe.log"
rm -f "/private/tmp/remove_printers.err.log"
# rm -f "/tmp/remove_printers.out.log"
# rm -f "/tmp/remove_printers.err.log"
rm -- "$0"
exit
"""

    log("→ About to write termination script")
    try:
        with open("/tmp/pr_end.sh", "w") as f:
            f.write(plist_termination_script)
        log(f"✅ Termination script written to /tmp/pr_end.sh")
    except Exception as e:
        log(f"❌ Failed to write termination script: {e}")

    run(f"chmod +x /tmp/pr_end.sh", ignore_errors=True)
    run(f"chown {uid}:{gid} /tmp/pr_end.sh", ignore_errors=True)
    run('open -j -a Terminal "/tmp/pr_end.sh"')


if __name__ == "__main__":
    main()
