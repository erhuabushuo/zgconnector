import logging
import asyncio

import uvloop
import aioredis

from wlconnector.protocol import Protocol


class Server:
    def __init__(self, cfg, is_debug):
        """

        :param cfg: 配置项
        """
        self.cfg = cfg
        self.token = cfg.get('general', 'token')
        self.protocols = {}
        self.server_address = (cfg.get('general', 'listen_ip'), cfg.getint('general', 'listen_port'))
        self.expiration_time = cfg.getint('general', 'expiration_time')
        self.loop = uvloop.new_event_loop()
        if is_debug:
            self.loop.set_debug(True)
        task = self.loop.create_task(aioredis.create_pool('redis://{}:{}'.format(cfg.get('redis', 'host'), cfg.getint('redis', 'port')),
                                                          minsize=cfg.getint('redis', 'min_size'), maxsize=cfg.getint('redis', 'max_size'), loop=self.loop))
        task.add_done_callback(self.set_redis)
        factory = self.loop.create_server(lambda: Protocol(self), *self.server_address)
        self.server = self.loop.run_until_complete(factory)

    def set_redis(self, future):
        self.redis = future.result()

    def run(self):
        logging.info("Staring up on {} port {}".format(*self.server_address))
        try:
            self.loop.run_forever()
        finally:
            logging.info("Closing redis")
            self.redis.close()
            self.loop.run_until_complete(self.redis.wait_closed())
            logging.info("Closing server")
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            logging.info("Closing event loop")
            self.loop.close()

