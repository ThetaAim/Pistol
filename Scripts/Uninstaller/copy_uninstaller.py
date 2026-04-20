import os
import shutil
from Tools.tools import to_absolute
import pwd


def copy_uninstaller_app():
    source_app = to_absolute("../pkgs/Uninstaller/prim_end.app")
    dest_dir = os.path.expanduser("~/Library/Application Support/Pistol")
    dest_app = os.path.join(dest_dir, "prim_end.app")

    os.makedirs(dest_dir, exist_ok=True)

    # Remove existing bundle if it exists
    if os.path.exists(dest_app):
        shutil.rmtree(dest_app)

    # Copy and resolve symlinks
    shutil.copytree(source_app, dest_app, symlinks=False)
    print(f"✅ Copied uninstaller app to: {dest_app}")

    # Optional: Set ownership to current user (for security hygiene)
    try:
        username = os.getenv("USER")
        if username:
            uid = pwd.getpwnam(username).pw_uid
            gid = pwd.getpwnam(username).pw_gid

            for root, dirs, files in os.walk(dest_app):
                os.chown(root, uid, gid)
                for d in dirs:
                    os.chown(os.path.join(root, d), uid, gid)
                for f in files:
                    os.chown(os.path.join(root, f), uid, gid)
            print(f"🔐 Ownership set to user '{username}'")
    except Exception as e:
        print(f"[!] Could not set ownership: {e}")
