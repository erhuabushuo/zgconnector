import sys
import configparser
import logging
import warnings

import click

from zgconnector.server import Server


@click.command()
@click.argument('config_path', default='/etc/zgconnector.ini')
def cli(config_path):
    """智国TCP通信服务器"""
    cfg = configparser.ConfigParser()
    cfg.read(config_path)

    is_debug = cfg.getboolean('general', 'debug')

    logging.basicConfig(
        level=logging.DEBUG if is_debug else logging.INFO,
        format='%(asctime)s %(name)-4s %(levelname)-4s %(message)s',
        stream=sys.stdout,
    )

    if is_debug:
        warnings.simplefilter('always', ResourceWarning)

    server = Server(cfg, is_debug)
    server.run()


if __name__ == "__main__":
    cli()