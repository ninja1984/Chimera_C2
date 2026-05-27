#!/home/dan/Chimera_Project/venv/bin/python3
from scapy.all import IP, TCP, send, fragment
import sys
import os
import json
import time
from datetime import datetime

class FragmentationTester:
    """
    Agent 107: IDS/IPS Reassembly Auditor.
    Tests if the target's security layer correctly reassembles 
    fragmented IP packets or if it can be bypassed via 'Fragment Overlap'.
    """
    def __init__(self, target, port=80):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/107_Fragmentation_Tester/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def test_reassembly(self, frag_size=8):
        """Sends a fragmented TCP SYN to test basic reassembly."""
        print(f"[*] AGENT 107: Sending fragmented TCP SYN to {self.target}:{self.port}...")
        try:
            # Craft a standard TCP SYN
            ip = IP(dst=self.target)
            tcp = TCP(sport=12345, dport=self.port, flags="S", seq=1000)
            pkt = ip/tcp
            
            # Fragment the packet into tiny pieces
            frags = fragment(pkt, fragsize=frag_size)
            
            # Send fragments with a slight delay between them
            for f in frags:
                send(f, verbose=False)
                time.sleep(0.1)
                
            return True
        except Exception as e:
            print(f"    [!] Scapy Injection Failed: {e}")
            return False

    def execute(self):
        print(f"--- [AGENT 107: FRAGMENTATION ANALYSIS - {self.target}] ---")
        
        # We test basic reassembly first
        success = self.test_reassembly()
        
        detection = "CLEAN" if success else "INJECTION_ERROR"
        
        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/frag_test_{self.target}_{timestamp}.json"
        
        payload = {
            "target": self.target,
            "port": self.port,
            "fragment_size": 8,
            "timestamp": str(datetime.now()),
            "status": detection
        }
        
        with open(loot_file, 'w') as f:
            json.dump(payload, f, indent=4)
            
        print(f"[!!!] EVASION INTELLIGENCE LOGGED: {loot_file}")
        print("[*] Note: If the target still responds to Agent 10, the WAF/IPS is reassembling correctly.")
        return payload

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
        
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 80
    FragmentationTester(target, port).execute()
