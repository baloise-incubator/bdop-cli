from typing import Union, Optional
from .command import Command
from .sync_apps import SyncAppsCommand
from .version import VersionCommand

CommandArgs = Union[
    SyncAppsCommand.Args,
    VersionCommand.Args,
]


class CommandFactory:
    @staticmethod
    def create(args: CommandArgs) -> Command:
        command: Optional[Command]
        if isinstance(args, SyncAppsCommand.Args):
            command = SyncAppsCommand(args)
        elif isinstance(args, VersionCommand.Args):
            command = VersionCommand(args)
        return command
