#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import time
import json
import random
from datetime import datetime

class PortKnockerPro:
    """
    Agent 16 Pro: Multi-Sequence Adversarial Knocker.
    Tests common default sequences and custom permutations to trigger 
    hidden services protected by knock-daemons.
    """
    def __init__(self, target):
        self.target = target
        self.loot_dir = "/home/dan/Chimera_Project/agents/16_Port_Knocker/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        
        # Library of common 'Lazy Admin' default sequences
        self.sequence_library = {
            "default_sequential": ["7000:tcp", "8000:tcp", "9000:tcp"],
            "default_reverse": ["9000:tcp", "8000:tcp", "7000:tcp"],
            "low_port_combo": ["1:tcp", "2:tcp", "3:tcp"],
            "mikrotik_style": ["1111:tcp", "2222:tcp", "3333:tcp"],
            "udp_trigger": ["5123:udp", "6123:udp", "7123:udp"]
        }

    def _send_knock(self, port_proto, delay):
        """Low-level packet injection for a single 'tap'."""
        try:
            port_str, proto = port_proto.split(':')
            port = int(port_str)
            
            if proto.lower() == 'tcp':
                # Stealth SYN - we don't complete the handshake
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect_ex((self.target, port))
                s.close()
            else:
                # UDP Burst
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b"\x01", (self.target, port))
                s.close()
            
            # Jitter the timing slightly to evade basic sequencing detection
            time.sleep(delay + random.uniform(0.01, 0.05))
            return True
        except Exception as e:
            print(f"    [!] Tap Error on {port_proto}: {e}")
            return False

    def execute_sequence(self, name, sequence, delay=0.2):
        """Executes a specific named sequence of knocks."""
        print(f"[*] AGENT 16: Attempting Sequence [{name}] -> {sequence}")
        success_count = 0
        for item in sequence:
            if self._send_knock(item, delay):
                success_count += 1
        return success_count == len(sequence)

    def execute(self, custom_seq=None):
        print(f"--- [AGENT 16: PORT KNOCKER PRO - {self.target}] ---")
        
        results = {"target": self.target, "attempts": []}
        
        # 1. Execute Custom Sequence if provided
        if custom_seq:
            seq_list = custom_seq.split(',')
            self.execute_sequence("CUSTOM", seq_list)
            results["attempts"].append({"name": "CUSTOM", "seq": seq_list})
        
        # 2. Iterate through the Library
        else:
            for name, seq in self.sequence_library.items():
                self.execute_sequence(name, seq)
                results["attempts"].append({"name": name, "seq": seq})
                # Pause between different sequence attempts
                time.sleep(1)

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/knock_results_{self.target}_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump(results, f, indent=4)
            
        print(f"[!!!] KNOCK OPERATION FINISHED. DATA LOGGED: {loot_file}")
        print("[*] RECOMMENDATION: Run Agent 10 (Banner Grab) on common ports to see if any opened.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [optional_custom_sequence]")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    custom = sys.argv[2] if len(sys.argv) > 2 else None
    
    PortKnockerPro(target_ip).execute(custom)
