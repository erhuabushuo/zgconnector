import logging
import time
import json

from wlconnector.packet import Packet
from wlconnector.cmd import Cmd

async def heartbeat(protocol):
    """
    处理心跳包
    :param protocol: Protocol
    :return:
    """
    from_ = protocol.packet.from_
    try:
        last_protocol = protocol.server.protocols[from_]
        if last_protocol != protocol:
            logging.debug(f"close last connection with {from_} @ f{last_protocol.transport.get_extra_info('peername')}")
            last_protocol.transport.close()
            del protocol.server.protocols[from_]
    except KeyError:
        pass

    protocol.server.protocols[from_] = protocol

    protocol.heartbeat_at = time.time()

    redis_key = f'{from_}_heartbeat'
    redis_value = {
        'uid': from_,
        'ver': protocol.packet.ver,
        'client_address': protocol.transport.get_extra_info('peername'),
        'server_address': protocol.server.conn_ip,

    }
    await protocol.server.redis.execute('setex', redis_key, protocol.server.expiration_time, json.dumps(redis_value))

    packet = Packet(protocol.packet.ver, protocol.server.token, from_, from_, Cmd.REPLY, 0)
    pack = packet.pack()
    protocol.transport.write(pack)



