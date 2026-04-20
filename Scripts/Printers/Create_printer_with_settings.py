import os
import subprocess


def run_command(command):
    try:
        result = os.system(command)
        if result == 0:
            print(f"Command succeeded")
        else:
            print(f"Command failed: {result}")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")


def create_printer(printer_name, ip_address, queue, ppd_path, location="", **settings):
    # Add the printer using sqport
    command = f"lpadmin -p '{printer_name}' -v 'sqport://{ip_address}/{queue}' -L '{location}' -P '{ppd_path}' -E -o printer-is-shared=false"
    run_command(command)

    # this phase adds more kwagrs if passed
    
    for key, value in settings.items():

        # Set the Wide Large Capacity Tray option. lpadmin adds extra values to the main values
        set_tray_command = f"lpadmin -p {printer_name} -o {key}={value}"
        run_command(set_tray_command)



