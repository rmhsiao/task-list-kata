from typing import cast

from task_list import dtos
from task_list.console import Console
from task_list.enums import CommandName
from task_list.task import Task


class CommandParser:

    command_map: dict[
        str,
        type[dtos.Command] | dict[str, type[dtos.Command]]
    ] = {
        CommandName.SHOW: dtos.ShowCommand,
        CommandName.ADD: {
            'project': dtos.AddProjectCommand,
            'task': dtos.AddTaskCommand,
        },
        CommandName.CHECK: dtos.CheckTaskCommand,
        CommandName.UNCHECK: dtos.UncheckTaskCommand,
        CommandName.HELP: dtos.HelpCommand,
        CommandName.QUIT: dtos.QuitCommand,
    }

    def parse(self, command_line: str) -> dtos.Command:
        # ValueError: not enough values to unpack
        # TODO: add a custom error
        command_name, *rest_pieces = command_line.split()

        command_class_or_sub_map = self.command_map[command_name]

        if isinstance(command_class_or_sub_map, type):
            command_class = command_class_or_sub_map
            command = command_class(*rest_pieces)
        else:
            sub_command_name, *sub_command_args = rest_pieces
            sub_command_class = command_class_or_sub_map[sub_command_name]
            command = sub_command_class(*sub_command_args)

        return command


class TaskList:

    def __init__(self, console: Console) -> None:
        self.console = console
        self.last_id: int = 0
        self.tasks: dict[str, list[Task]] = dict()

        self.command_parser = CommandParser()

    def run(self) -> None:
        while True:
            command_line = self.console.input("> ")

            try:
                command = self.command_parser.parse(command_line)
            except (KeyError, ValueError):
                self.error(command_line)
                continue

            if command.name == CommandName.QUIT:
                break

            self.execute(command)

    def execute(self, command: dtos.Command) -> None:
        if command.name == CommandName.SHOW:
            self.show()
        elif command.name == CommandName.ADD:
            self.add(cast(dtos.AddProjectCommand, command))
        elif command.name == CommandName.CHECK:
            self.check(cast(dtos.CheckTaskCommand, command))
        elif command.name == CommandName.UNCHECK:
            self.uncheck(cast(dtos.UncheckTaskCommand, command))
        elif command.name == CommandName.HELP:
            self.help()

    def show(self) -> None:
        for project, tasks in self.tasks.items():
            self.console.print(project)
            for task in tasks:
                self.console.print(f"  [{'x' if task.is_done() else ' '}] "
                                   f"{task.id}: {task.description}")
            self.console.print()

    def add(
        self, command: dtos.AddProjectCommand | dtos.AddTaskCommand
    ) -> None:
        if command.sub_command == "project":
            self.add_project(cast(dtos.AddProjectCommand, command))
        elif command.sub_command == "task":
            self.add_task(cast(dtos.AddTaskCommand, command))

    def add_project(self, command: dtos.AddProjectCommand) -> None:
        self.tasks[command.project_name] = []

    def add_task(self, command: dtos.AddTaskCommand) -> None:
        project_tasks = self.tasks.get(command.project_name)
        if project_tasks is None:
            self.console.print("Could not find a project with the name "
                               f"{command.project_name}.")
            self.console.print()
            return
        project_tasks.append(Task(self.next_id(), command.description, False))

    def check(self, command: dtos.CheckTaskCommand) -> None:
        self.set_done(command, True)

    def uncheck(self, command: dtos.UncheckTaskCommand) -> None:
        self.set_done(command, False)

    def set_done(
        self,
        command: dtos.CheckTaskCommand | dtos.UncheckTaskCommand,
        done: bool
    ) -> None:
        id_ = int(command.task_id)
        for project, tasks in self.tasks.items():
            for task in tasks:
                if task.id == id_:
                    task.set_done(done)
                    return
        self.console.print(f"Could not find a task with an ID of {id_}")
        self.console.print()

    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def error(self, command_line: str) -> None:
        self.console.print("I don't know what the command "
                           f"'{command_line}' is.")
        self.console.print()

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id
