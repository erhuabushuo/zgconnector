import unittest

from zgconnector.packet import Packet, PACKET_SIZE
from zgconnector.cmd import Cmd


class TestPacket(unittest.TestCase):
    def test_pack(self):
        """
        测试打包大小
        :return:
        """
        packet = Packet(1, 'abcdef','abc', 'abc', 1, 1)
        pack = packet.pack()
        self.assertEqual(len(pack), PACKET_SIZE)

    def test_unpack(self):
        """
        测试解析包格式
        :return:
        """
        msg = b'\x00\x01abcdefabc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00abc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01'
        packet = Packet.unpack(msg)
        self.assertEqual(packet.ver, 1)
        self.assertEqual(packet.from_, 'abc')
        self.assertEqual(packet.to, 'abc')
        self.assertEqual(packet.cmd, Cmd.HEARTBEAT)
        self.assertEqual(packet.length, 1)
