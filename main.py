import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog

# import Data
from Scripts.Installer.tk_installer import install_pkgs
from Scripts.Printers.Create_printer_with_settings import create_printer
from Scripts.Presets.Copy_Prst import copy_files
from Data.Data import packages, printer_configs
from Tools.tools import to_absolute
# from Scripts.Uninstaller.copy_uninstaller import copy_uninstaller_app
# from Scripts.Uninstaller.Generate_plist import generate_a_plist

# Initialize global variables
install_thread = None
install_event = None


def on_closing():
    if install_thread is not None and install_thread.is_alive():
        messagebox.showinfo("Wait", "Installation is still running. Please wait until it finishes.")
    else:

        main_window.destroy()

        # Get full .app bundle path
        app_bundle_path = os.path.abspath(os.path.join(sys.executable, "..", "..", ".."))
        subprocess.Popen(
            ['sh', '-c', f'sleep 3 && rm -rf "{app_bundle_path}"'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


def change_button_to_quit(install_button):
    install_button.config(text="Quit", state=tk.NORMAL, command=on_closing)


def run_installation(text_widget, install_button, event):
    # Disable the install button
    install_button.config(state=tk.DISABLED)

    # # A. Run Package Installer Setup files
    # ###############################################
    text_widget.insert(tk.END, "Starting Installation Process.\n")
    success = install_pkgs(packages, text_widget, event)
    if not success:
        return
    # B. Create Printers and set Settings
    ###############################################
    text_widget.insert(tk.END, "Setting up printers...\n")

    for config in printer_configs:
        text_widget.insert(tk.END, f"Setting up {config[0]}...\n")
        create_printer(*config[:5], **config[5])

    # D. Copy/Set Presets
    username = os.popen('whoami').read().strip()
    copy_files(to_absolute("../pkgs/Presets"), f"/Users/{username}/Library/Preferences")
    text_widget.insert(tk.END, "Copied presets successfully.\n")
    text_widget.insert(tk.END, "Installation complete.\n")

    # E. Copy Uninstaller

    # copy_uninstaller_app()
    # generate_a_plist()

    # Signal Event Done
    event.set()
    # Change the button to quit
    change_button_to_quit(install_button)


def start_installation_with_thread(text_widget, install_button):
    global install_thread, install_event
    install_event = threading.Event()
    install_thread = threading.Thread(target=run_installation, args=(text_widget, install_button, install_event))
    install_thread.start()


def main():
    global main_window

    pass_key = "1212"
    # pass_input ="1212"
    pass_input = tkinter.simpledialog.askstring("Authentication", "Enter password:", show='*')

    if pass_input == pass_key:

        main_window = tk.Tk()

        posx = 800  # X coordinate
        posy = 300  # Y coordinate
        main_window.geometry(f"+{posx}+{posy}")

        main_window.title("Pistol Printer Installer - By OREN Ohayon")

        main_window.protocol("WM_DELETE_WINDOW", on_closing)

        text_widget = tk.Text(main_window, wrap=tk.WORD, width=60, height=25)
        text_widget.pack(pady=10, padx=10)

        install_button = tk.Button(main_window, text="Start Installation",
                                   command=lambda: start_installation_with_thread(text_widget, install_button))
        install_button.pack(pady=10)

        main_window.mainloop()

    else:
        exit()


if __name__ == "__main__":
    main()
