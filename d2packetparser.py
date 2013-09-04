from construct import *
from d2packetparser_c2s import c2s_packets
from d2packetparser_s2c import s2c_packets


d2_packet_parser = (OptionalGreedyRange(c2s_packets), OptionalGreedyRange(s2c_packets))
