import sys
import configparser
import logging
import warnings


from wlconnector.server import Server


def main():
    cfg_file_path = '/etc/wlconnector.ini'
    if len(sys.argv) > 1:
        cfg_file_path = sys.argv[1]

    # load config file
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file_path)

    is_debug = cfg.getboolean('general', 'debug')

    logging.basicConfig(
        level=logging.DEBUG if is_debug else logging.INFO,
        format='%(asctime)s %(name)-4s %(levelname)-4s %(message)s',
        stream=sys.stdout,
    )

    if is_debug:
        warnings.simplefilter('always', ResourceWarning)

    # now starting server
    server = Server(cfg, is_debug)
    server.run()


if __name__ == "__main__":
    main()