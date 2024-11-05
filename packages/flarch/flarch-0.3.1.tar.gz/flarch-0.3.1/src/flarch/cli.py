import argparse

from flarch.commands.format_drive import format_drive
from flarch.commands.nullify_drive import nullify_drive
from flarch.commands.write_image import write_image
from flarch.utils.commands_exist import ensure_commands_exist

from flarch.__about__ import __version__


def main():
    parser = argparse.ArgumentParser(description="Work with floppies with ease!")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    parser.add_argument(
        "-v", "--version", action="store_true", help="Show program's version and exit"
    )

    # region Format floppy
    format_parser = subparsers.add_parser("format", help="Format the floppy into FAT")
    format_parser.add_argument("drive", type=str, help="Floppy drive")
    format_parser.add_argument(
        "-N",
        "--skip-nullification",
        action="store_true",
        help="Skip drive nullification. Faster, but the resulting floppy may work unexpectedly",
    )
    # endregion

    # region Nullify floppy
    nullify_parser = subparsers.add_parser(
        "nullify", help="Turn all floppy sectors into zeroes"
    )
    nullify_parser.add_argument("drive", type=str, help="Floppy drive")
    # endregion

    # region Write image
    write_parser = subparsers.add_parser(
        "write", help="Turn all floppy sectors into zeroes"
    )
    write_parser.add_argument(
        "-from", "--image-from", type=str, help=".img file", required=True
    )
    write_parser.add_argument(
        "-to", "--drive-to", type=str, help="Floppy drive", required=True
    )
    write_parser.add_argument(
        "-N",
        "--skip-nullification",
        action="store_true",
        help="Skip drive nullification. Faster, but the resulting floppy may work unexpectedly",
    )
    # endregion

    args = parser.parse_args()

    ensure_commands_exist(["blockdev", "mkfs.vfat", "dd", "pv"])

    if args.version:
        print(__version__)
        return

    if args.command == "nullify":
        nullify_drive(args.drive)

    elif args.command == "format":
        if not args.skip_nullification:
            nullify_drive(args.drive)

        format_drive(args.drive)

    elif args.command == "write":
        if not args.skip_nullification:
            nullify_drive(args.drive_to)

        write_image(image_path=args.image_from, drive=args.drive_to)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
