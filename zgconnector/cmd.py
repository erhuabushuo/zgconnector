from enum import Enum


class Cmd(Enum):
    HEARTBEAT = 1
    REPLY = 2
    ERROR = 3
    AD = 4