import os
import shlex


def write_image(image_path, drive):
    image_size = os.path.getsize(image_path)

    image_path = shlex.quote(image_path)
    drive = shlex.quote(drive)

    print(f"Started writing '{image_path}' image to '{drive}'")
    os.system(f"dd if={image_path} | pv -s {image_size} | dd of={drive}")
