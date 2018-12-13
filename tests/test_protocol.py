import unittest
from unittest.mock import Mock, patch

from zgconnector.protocol import Protocol
from zgconnector.packet import Packet
from zgconnector.cmd import Cmd

class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.transportMock = Mock()
        self.serverMock = Mock()
        self.serverMock.token = 'abcdef'
        self.protocol = Protocol(self.serverMock)
        self.protocol.connection_made(self.transportMock)

    @patch('zgconnector.protocol.commands')
    def test_heartbeat(self, mock_commands):
        """
        测试心跳包
        :param mock_commands:
        :return:
        """
        packet = Packet(1, 'abcdef', 'abc', 'abc', Cmd.HEARTBEAT, 0)
        pack = packet.pack()
        self.protocol.data_received(pack)
        # 测试Token一致
        self.assertEqual(packet.token, self.serverMock.token)

        mock_commands.get.assert_called_with(Cmd.HEARTBEAT)


    @patch('zgconnector.protocol.commands')
    @patch('zgconnector.protocol.transfer')
    def test_transfer(self, mock_transfer, mock_commands):
        """
        测试消息转发
        :param mock_commands:
        :return:
        """
        packet = Packet(1, 'abcdef','abc', 'efc', 10, 0)
        pack = packet.pack()
        mock_commands.get.return_value = None
        self.protocol.data_received(pack)

        mock_commands.get.assert_called_with(10)
        self.serverMock.loop.create_task.assert_called_with(mock_transfer())

