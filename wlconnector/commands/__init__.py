
from .heartbeat import heartbeat
from .transfer import transfer

from wlconnector.cmd import Cmd

commands ={
    Cmd.HEARTBEAT: heartbeat,
}