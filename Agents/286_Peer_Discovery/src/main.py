#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import struct
import binascii
import os
import threading
import time

class RawPeerDiscovery:
    """
    Agent 501 (Hardened): Raw Socket ARP Injector.
    Manually constructs and injects Ethernet/ARP frames to 
    map the subnet. Operates entirely below the TCP/IP stack.
    """
    def __init__(self, interface="eth0"):
        self.interface = interface
        self.active_hosts = set()
        self.scanning = True

    def get_mac_address(self):
        """Actionable: Reads physical MAC from sysfs."""
        path = f"/sys/class/net/{self.interface}/address"
        with open(path, "r") as f:
            return f.read().strip()

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except: ip = '127.0.0.1'
        finally: s.close()
        return ip

    def _listen_for_replies(self, raw_socket):
        """Dedicated thread to catch ARP replies (Opcode 2)."""
        while self.scanning:
            try:
                raw_socket.settimeout(1.0)
                packet = raw_socket.recvfrom(2048)[0]
                
                # Unpack Ethernet Header (First 14 bytes)
                eth_header = packet[0:14]
                eth_dict = struct.unpack("!6s6sH", eth_header)
                eth_protocol = socket.ntohs(eth_dict[2])

                # 0x0806 is the ARP protocol
                if eth_protocol == 8: 
                    # Unpack ARP Header (Bytes 14 to 42)
                    arp_header = packet[14:42]
                    arp_detailed = struct.unpack("!HHBBH6s4s6s4s", arp_header)
                    
                    opcode = arp_detailed[4]
                    if opcode == 2: # ARP Reply
                        sender_mac = binascii.hexlify(arp_detailed[5]).decode('ascii')
                        sender_ip = socket.inet_ntoa(arp_detailed[6])
                        
                        if sender_ip not in self.active_hosts:
                            self.active_hosts.add(sender_ip)
                            print(f"[\033[92mPEER CONFIRMED\033[0m] IP: {sender_ip} | MAC: {sender_mac}")
                            self._update_swarm_cache(sender_ip, sender_mac)
            except socket.timeout:
                continue
            except Exception as e:
                pass

    def arp_sweep(self):
        print(f"--- [AGENT 501: RAW ARP SWARM DISCOVERY] ---")
        if os.getuid() != 0:
            print("[!] Critical: Raw socket injection requires Root.")
            return

        local_ip = self.get_local_ip()
        local_mac = self.get_mac_address()
        base_ip = ".".join(local_ip.split(".")[:-1])
        
        print(f"[*] Origin: {local_ip} ({local_mac}) on {self.interface}")
        print(f"[*] Initiating hardware-level sweep on {base_ip}.0/24...")

        try:
            # Create the raw AF_PACKET socket (ETH_P_ARP = 0x0806)
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
            s.bind((self.interface, 0))

            # Start the listener thread
            listener = threading.Thread(target=self._listen_for_replies, args=(s,))
            listener.start()

            # --- MANUALLY PACKING THE FRAMES ---
            # Ethernet Header
            eth_dest = binascii.unhexlify('ffffffffffff') # Broadcast MAC
            eth_src = binascii.unhexlify(local_mac.replace(':', ''))
            eth_type = struct.pack('!H', 0x0806) # ARP
            eth_frame = eth_dest + eth_src + eth_type

            # ARP Header Constants
            arp_hw_type = struct.pack('!H', 1)       # Ethernet
            arp_proto_type = struct.pack('!H', 0x0800) # IPv4
            arp_hw_len = struct.pack('!B', 6)        # MAC length
            arp_proto_len = struct.pack('!B', 4)     # IP length
            arp_opcode = struct.pack('!H', 1)        # ARP Request
            arp_sender_mac = eth_src
            arp_sender_ip = socket.inet_aton(local_ip)
            arp_target_mac = binascii.unhexlify('000000000000') # Blank for request

            # Blast the subnet
            for i in range(1, 255):
                target_ip = f"{base_ip}.{i}"
                if target_ip == local_ip: continue
                
                arp_target_ip = socket.inet_aton(target_ip)
                
                arp_packet = (arp_hw_type + arp_proto_type + arp_hw_len + 
                              arp_proto_len + arp_opcode + arp_sender_mac + 
                              arp_sender_ip + arp_target_mac + arp_target_ip)
                
                # Combine Ethernet Frame + ARP Packet and Inject
                s.send(eth_frame + arp_packet)
                time.sleep(0.01) # Micro-jitter to prevent dropping packets

            # Allow 2 seconds for late replies to arrive
            time.sleep(2)
            self.scanning = False
            listener.join()
            s.close()
            
            print(f"[*] Sweep complete. Found {len(self.active_hosts)} potential targets.")

        except Exception as e:
            print(f"[!] Injection failed: {e}")

    def _update_swarm_cache(self, ip, mac):
        with open("/tmp/.swarm_topology", "a") as f:
            f.write(f"{ip},{mac}\n")

if __name__ == "__main__":
    RawPeerDiscovery().arp_sweep()
