
from dataclasses import dataclass
from typing import ClassVar

from task_list.enums import CommandName


@dataclass
class Command:
    name: ClassVar[CommandName]


@dataclass
class ShowCommand(Command):
    name: ClassVar[CommandName] = CommandName.SHOW


@dataclass
class AddProjectCommand(Command):
    name: ClassVar[CommandName] = CommandName.ADD
    sub_command: ClassVar[str] = 'project'

    project_name: str


@dataclass
class AddTaskCommand(Command):
    name: ClassVar[CommandName] = CommandName.ADD
    sub_command: ClassVar[str] = 'task'

    project_name: str
    description: str


@dataclass
class CheckTaskCommand(Command):
    name: ClassVar[CommandName] = CommandName.CHECK

    task_id: str


@dataclass
class UncheckTaskCommand(Command):
    name: ClassVar[CommandName] = CommandName.UNCHECK

    task_id: str


@dataclass
class HelpCommand(Command):
    name: ClassVar[CommandName] = CommandName.HELP


@dataclass
class QuitCommand(Command):
    name: ClassVar[CommandName] = CommandName.QUIT
