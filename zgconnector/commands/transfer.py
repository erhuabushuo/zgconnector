import time

from zgconnector.packet import Packet
from zgconnector.cmd import Cmd

async def transfer(protocol):
    """
    处理消息转发
    :param protocol: Protocol
    :return:
    """
    packet = Packet(protocol.packet.ver, protocol.server.token, protocol.packet.app_id, protocol.packet.from_, protocol.packet.to, protocol.packet.cmd, protocol.packet.length)
    packet.body = protocol.packet.body
    pack = packet.pack()

    protocol.server.protocols[protocol.packet.from_] = protocol
    protocol.heartbeat_at = time.time()

    try:
        to_protocol = protocol.server.protocols[protocol.packet.to]
        to_protocol.transport.write(pack)
        to_protocol.transport.write(packet.body)
    except KeyError:
        body = f"{protocol.packet.to} is offline!".encode('utf-8')
        packet = Packet(protocol.packet.ver, protocol.server.token, protocol.packet.app_id, protocol.packet.from_, protocol.packet.to, Cmd.ERROR, len(body))
        pack = packet.pack()
        protocol.transport.write(pack)
        protocol.transport.write(body)
        protocol.transport.close()


