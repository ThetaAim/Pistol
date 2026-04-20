import os
import sys
import pwd

username = os.getenv('USER') or os.popen('whoami').read().strip()
uid = pwd.getpwnam(username).pw_uid
gid = pwd.getpwnam(username).pw_gid



def to_absolute(relative_path):
    return os.path.abspath(os.path.join(find_base_dir(), relative_path))


def find_base_dir():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles put resources in _MEIPASS
        return os.path.join(sys._MEIPASS, 'Resources')
    else:
        # Use the script's actual folder to resolve ../pkgs
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(script_dir, "../pkgs"))


source_app = to_absolute('../pkgs/Uninstaller/printer_uninst.app')
destination_app = "/usr/local/bin/printer_uninst.app"

# Build AppleScript command as a single-line string (escaped properly)
copy_uninstaller = (
    f'do shell script "cp -R \'{source_app}\' \'{destination_app}\' && '
    f'chown -R $(whoami):staff \'{destination_app}\' && '
    f'chmod -R 755 \'{destination_app}\'" with administrator privileges\n'
)

# def find_base_dir():
#     if hasattr(sys, '_MEIPASS'):
#         # If running as a PyInstaller app
#         base_dir = os.path.join(sys._MEIPASS, 'Resources')
#     else:
#         # Adjusting for parent directory
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         base_dir = "../pkgs/"  # Move up one directory
#     return base_dir

# Test Purpose
# base_dir = find_base_dir()  # Call the function to get the base directory
# print("Base Directory:", base_dir)  # Print the result
