
from enum import Enum


class CommandName(str, Enum):
    SHOW = 'show'
    ADD = 'add'
    CHECK = 'check'
    UNCHECK = 'uncheck'
    HELP = 'help'
    QUIT = 'quit'
