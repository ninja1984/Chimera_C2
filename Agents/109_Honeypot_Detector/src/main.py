#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
import time
from datetime import datetime

class HoneypotDetector:
    """
    Agent 102: Deception & Trap Identifier.
    Tests for high-interaction honeypot signatures such as 
    Infinite Buffers and 'Accept-All' credential logic.
    """
    def __init__(self, target, port):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/102_Honeypot_Detector/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def test_infinite_buffer(self):
        """Sends a large junk payload to see if the server 'swallows' it indefinitely."""
        print(f"[*] Testing Infinite Buffer on {self.target}:{self.port}...")
        try:
            with socket.create_connection((self.target, self.port), timeout=5) as s:
                # Send 10KB of junk
                payload = b"A" * 10240
                s.sendall(payload)
                # If it doesn't error out or close, it's suspicious
                return True
        except Exception:
            return False

    def test_latency_jitter(self):
        """Measures response consistency. Virtual honeypots often have 'Artificial' latency."""
        samples = []
        for _ in range(5):
            start = time.time()
            try:
                with socket.create_connection((self.target, self.port), timeout=2):
                    samples.append(time.time() - start)
            except: pass
        
        if len(samples) < 2: return 0
        # Calculate variance
        avg = sum(samples) / len(samples)
        variance = sum((x - avg) ** 2 for x in samples) / len(samples)
        return variance

    def execute(self):
        print(f"--- [AGENT 102: HONEYPOT DETECTION - {self.target}:{self.port}] ---")
        
        is_suspicious = False
        buffer_result = self.test_infinite_buffer()
        jitter = self.test_latency_jitter()
        
        findings = []
        if buffer_result:
            findings.append("INFINITE_BUFFER_SINK")
        if jitter < 0.0001: # Too perfect, likely a script-based response
            findings.append("SUSPICIOUSLY_CONSISTENT_LATENCY")
        
        if len(findings) > 1:
            is_suspicious = True
            print("[!!!] WARNING: TARGET PORT EXHIBITS HONEYPOT BEHAVIOR.")
            for f in findings:
                print(f"    [!] Signature: {f}")

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/honey_{self.target}_{self.port}.json"
        with open(loot_file, 'w') as f:
            json.dump({
                "target": self.target,
                "port": self.port,
                "suspicious": is_suspicious,
                "signatures": findings
            }, f, indent=4)
            
        return is_suspicious

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./main.py <target_ip> <port>")
        sys.exit(1)
        
    HoneypotDetector(sys.argv[1], sys.argv[2]).execute()
