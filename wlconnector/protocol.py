import asyncio
import logging
import time

from wlconnector.state import State
from wlconnector.packet import Packet, PACKET_SIZE
from wlconnector.commands import commands, transfer
from wlconnector.exceptions import PacketException


class Protocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
        self._buffer = bytearray()
        self.state = State.INIT
        self.heartbeat_at = time.time()
        self.packet = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self._buffer += data
        while self._buffer:
            if self.state == State.INIT:
                if len(self._buffer) < PACKET_SIZE:
                    return
                msg, self._buffer = self._buffer[:PACKET_SIZE], self._buffer[PACKET_SIZE:]
                try:
                    self.packet = Packet.unpack(msg)
                except PacketException:
                    logging.debug(f'failed to parse message: {msg}')
                    self.state = State.INIT
                    self.transport.close()
                    return
                if self.packet.token != self.server.token:
                    logging.debug(f"invalid token: {self.packet.token}")
                    self.transport.close()
                logging.debug(f"cmd: {self.packet.cmd} from {self.packet.from_} to {self.packet.to}")
                self.state = State.REQUEST
            if self.state == State.REQUEST:
                if len(self._buffer) < self.packet.length:
                    return
                msg, self._buffer = self._buffer[:self.packet.length], self._buffer[self.packet.length:]
                self.packet.body = msg
                logging.debug(f"content: {self.packet.body}")
                logging.debug(commands)
                command = commands.get(self.packet.cmd) or transfer
                self.server.loop.create_task(command(self))
                self.state = State.INIT


    def eof_received(self):
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, exc):
        try:
            del self.server.protocols[self.packet.from_]
        except IndexError:
            pass
        super().connection_lost(exc)