#!/home/dan/Chimera_Project/venv/bin/python3
import subprocess
import sys
import os
import json
import time
from datetime import datetime

class SentinelMonitor:
    """
    Agent 101: Environmental Health & Defense Monitor.
    Tracks RTT (Round Trip Time) and Packet Loss to detect 
    Active Defense (WAF/IDS) triggering or 'Tarpitting'.
    """
    def __init__(self, target):
        self.target = target
        self.loot_dir = "/home/dan/Chimera_Project/agents/101_Sentinel_Monitor/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.history = []

    def probe_health(self):
        """Perform a latency/loss probe to check connection stability."""
        try:
            # Send 5 ICMP packets
            result = subprocess.run(
                ['ping', '-c', '5', '-W', '2', self.target],
                capture_output=True, text=True
            )
            
            output = result.stdout
            stats = {
                "timestamp": str(datetime.now()),
                "loss_percent": 100.0,
                "avg_rtt": 0.0,
                "status": "OFFLINE"
            }

            if result.returncode == 0:
                # Parse packet loss
                if "packet loss" in output:
                    loss = output.split('%')[0].split()[-1]
                    stats["loss_percent"] = float(loss)
                
                # Parse RTT
                if "rtt min/avg/max" in output:
                    rtt = output.split('/')[-3]
                    stats["avg_rtt"] = float(rtt)
                
                stats["status"] = "HEALTHY" if stats["loss_percent"] < 20 else "DEGRADED"
                
            return stats
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}

    def execute(self, interval=10, duration=60):
        """Run continuous monitoring for a set duration."""
        print(f"--- [AGENT 101: SENTINEL HEALTH MONITOR - {self.target}] ---")
        
        end_time = time.time() + duration
        while time.time() < end_time:
            health = self.probe_health()
            self.history.append(health)
            
            status_symbol = "[+]" if health["status"] == "HEALTHY" else "[!]"
            print(f"    {status_symbol} {health['timestamp']} | RTT: {health['avg_rtt']}ms | Loss: {health['loss_percent']}%")
            
            if health["loss_percent"] > 50:
                print("    [!!!] CRITICAL: HIGH PACKET LOSS. IDS/WAF MAY BE DROPPING TRAFFIC.")
            
            time.sleep(interval)

        # Intelligence Commitment
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/health_{self.target}_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump(self.history, f, indent=4)
            
        print(f"[!!!] DEFENSIVE LANDSCAPE DATA STORED: {loot_file}")
        return self.history

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip>")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    SentinelMonitor(target_ip).execute()
