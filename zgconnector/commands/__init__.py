
from .heartbeat import heartbeat
from .transfer import transfer

from zgconnector.cmd import Cmd

commands ={
    Cmd.HEARTBEAT: heartbeat,
}