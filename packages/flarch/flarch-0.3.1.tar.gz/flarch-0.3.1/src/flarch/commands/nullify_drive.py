import shlex
import os

from flarch.utils.size_of_drive import size_of_drive


BLOCK_SIZE = 1024


def nullify_drive(drive_name):
    drive_name = shlex.quote(drive_name)
    drive_size_in_bytes = size_of_drive(drive_name)
    blocks_count = int(drive_size_in_bytes / BLOCK_SIZE)

    print(f"Nullification of '{drive_name}' has started")
    os.system(
        f"dd if=/dev/zero bs=1024 count={blocks_count} | pv -s {drive_size_in_bytes} | dd of={drive_name}"
    )
