import asyncio
import functools
import logging
import sys
import struct

from wlconnector.packet import Packet

SERVER_ADDRESS = ('localhost', 9700)
FMT = "!h6s40s40shL"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class EchoClient(asyncio.Protocol):
    def __init__(self, future):
        super().__init__()
        self.log = logging.getLogger('EchoClient')
        self.f = future

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connectiong to {} port {}'.format(*self.address)
        )

        self.message = struct.pack(FMT, 1, "abcdef", b"efg", b"efg", 1, 1)
        transport.write(self.message)
        transport.write(b'p')
        self.log.debug('sending {!r}'.format(self.message))


    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))
        packet = Packet.unpack(data)
        print(packet.cmd)

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connnection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connectiong_lost(exc)


client_completed = asyncio.Future()
client_factory = functools.partial(
    EchoClient,
    future=client_completed
)
factory_coroutine = event_loop.create_connection(
    client_factory,
    *SERVER_ADDRESS,
)

log.debug('waiting for client to complete')
try:
    event_loop.run_until_complete(factory_coroutine)
    event_loop.run_until_complete(client_completed)
finally:
    log.debug('closing event loop')
    event_loop.close()