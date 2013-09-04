import select
import socket
import d2crypt
import d2packetparser
import collections
import multiprocessing
from construct.protocols.ipstack import layer3_ipv4


class SojWatcher(multiprocessing.Process):

    def __init__(self, server_ips, server_ports, queue):

        multiprocessing.Process.__init__(self, daemon=True)
        self.queue = queue

        self.server_ips = server_ips
        self.server_ports = server_ports


    def run(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sock.bind((socket.gethostbyname(socket.gethostname()), 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        decryptors = collections.defaultdict(d2crypt.Decrypter)

        while True:

            if select.select([sock], [], [])[0]:

                ip_packet = layer3_ipv4.parse(sock.recv(65536))

                if ip_packet.header.protocol is "TCP":

                    iph, tcph, data = ip_packet.header, ip_packet.next.header, ip_packet.next.next

                    if iph.source in self.server_ips and str(tcph.source) in self.server_ports:

                        ip = iph.source
                        decrypted_data = (data,)

                        if data != b"\xaf\x01":

                            decrypted_data = decryptors[tcph.destination].decrypt(data)

                        else:

                            decryptors[tcph.destination] = d2crypt.Decrypter()

                        for ddata in decrypted_data:

                            for packet in d2packetparser.d2_packet_parser[1].parse(ddata):

                                if packet.fun is "chat":

                                    msg = str.lower(str(packet.message, encoding="ascii"))
                                    soj_count = None

                                    if "jordan" in msg:

                                        soj_count = int(str.split(msg)[0])

                                    elif "walks" in msg:

                                        soj_count = -1

                                    if soj_count:

                                        self.queue.put_nowait((soj_count, ip))
