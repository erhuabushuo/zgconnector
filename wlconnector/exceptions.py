
import struct

class PacketException(struct.error):
    pass

class OfflineException(KeyError):
    pass