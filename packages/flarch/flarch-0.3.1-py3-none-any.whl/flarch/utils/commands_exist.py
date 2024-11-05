import shutil
from typing import Iterable


def ensure_commands_exist(commands: Iterable[str]):
    not_available_commands = []

    for cmd in commands:
        path_to_cmd = shutil.which(cmd)

        if path_to_cmd is None:
            not_available_commands.append(cmd)

    if len(not_available_commands) > 0:
        raise Exception(
            "These commands must be available on your system in order to let the program work: "
            + ", ".join(not_available_commands)
        )
