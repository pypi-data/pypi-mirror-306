import os
import shlex


def format_drive(drive_name):
    drive_name = shlex.quote(drive_name)

    print(f"Started writing filesystem on '{drive_name}'")
    os.system(f"mkfs.vfat -v {drive_name}")
