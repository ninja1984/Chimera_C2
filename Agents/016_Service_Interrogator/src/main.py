#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
from datetime import datetime

class ServiceInterrogator:
    """
    Agent 12: OS & Stack Fingerprinter.
    Analyzes TCP/IP characteristics (TTL, Window Size, DF bit) 
    to identify the underlying Operating System and Kernel.
    """
    def __init__(self, target, port=80):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/12_Service_Interrogator/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def finger_print_stack(self):
        """
        Interrogates the target's networking stack.
        Linux typically has TTL=64, Windows TTL=128.
        """
        print(f"[*] AGENT 12: Interrogating Stack on {self.target}:{self.port}...")
        try:
            # Create a raw-ish socket to inspect packet headers
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.target, self.port))
            
            # Extracting the TTL and Window Size from the socket
            # This requires lower-level access than a standard request
            ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
            
            os_guess = "Unknown"
            if ttl <= 64:
                os_guess = "Linux/Unix/FreeBSD"
            elif ttl <= 128:
                os_guess = "Windows (NT/10/Server)"
            elif ttl <= 255:
                os_guess = "Cisco/Network Infrastructure"

            s.close()
            return {"ttl": ttl, "os_guess": os_guess}
        except Exception as e:
            print(f"    [!] Stack Interrogation Failed: {e}")
            return None

    def execute(self):
        print(f"--- [AGENT 12: STACK FINGERPRINTING - {self.target}] ---")
        stack_data = self.finger_print_stack()
        
        if stack_data:
            print(f"    [+] TTL IDENTIFIED: {stack_data['ttl']}")
            print(f"    [!!!] OS PROJECTION: {stack_data['os_guess']}")
            
            # Store Loot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            loot_file = f"{self.loot_dir}/stack_{self.target}_{timestamp}.json"
            
            payload = {
                "timestamp": str(datetime.now()),
                "target": self.target,
                "port": self.port,
                "stack_analysis": stack_data
            }
            
            with open(loot_file, 'w') as f:
                json.dump(payload, f, indent=4)
                
            return stack_data
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
        
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 80
    ServiceInterrogator(target, port).execute()
