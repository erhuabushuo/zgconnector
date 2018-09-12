import struct

from wlconnector.cmd import Cmd

"""
+---------+---------+----------+----------+---------+---------+----------------+
| Ver     | Token   | From     | To       | Cmd     | Length  | Body           |
+---------+---------+----------+----------+---------+---------+----------------+
| 2 bytes | 6 bytes | 40 bytes | 40 bytes | 2 bytes | 4 bytes | N length bytes |
+---------+---------+----------+----------+---------+---------+----------------+
"""

FMT = "!h6s40s40shL"   #h -> short 2 , L -> unsigned long 4
PACKET_SIZE = struct.calcsize(FMT)


class Packet:
    def __init__(self, ver, token, from_, to, cmd, length):
        self.ver = ver
        self.token = token
        self.from_ = from_
        self.to = to
        self.cmd = cmd
        self.length = length

    def pack(self):
        if isinstance(self.cmd, Cmd):
            _cmd = self.cmd.value
        else:
            _cmd = self.cmd
        return struct.pack(FMT, self.ver, self.token.encode('utf-8'), self.from_.encode('utf-8'), self.to.encode('utf-8'), _cmd, self.length)

    @staticmethod
    def unpack(data):
        pack = struct.unpack(FMT, data)
        try:
            _cmd = Cmd(pack[4])
        except ValueError:
            _cmd = pack[4]
        packet = Packet(pack[0], pack[1].decode('utf-8'), pack[2].decode('utf-8').rstrip('\0'), pack[3].decode('utf-8').rstrip('\0'), _cmd, pack[5])
        return packet

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

