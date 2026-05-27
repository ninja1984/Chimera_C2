#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import subprocess

class PersistenceWatchdog:
    """
    Agent 316: The Undead Sentinel.
    Monitors the status of critical Chimera agents and 
    automatically reinstantiates them if they are terminated.
    """
    def __init__(self, target_agents):
        # List of paths to the main.py of other agents
        self.targets = target_agents

    def _is_running(self, script_path):
        """Checks the process tree for the specific agent script."""
        try:
            output = subprocess.check_output(["ps", "aux"]).decode()
            return script_path in output
        except:
            return False

    def monitor_loop(self):
        print(f"--- [AGENT 316: WATCHDOG ACTIVE] ---")
        print(f"[*] Guarding {len(self.targets)} agents...")
        
        # Daemonize to background
        if os.fork() > 0: sys.exit(0)

        while True:
            for agent_path in self.targets:
                if not self._is_running(agent_path):
                    print(f"[!] Agent Terminated: {agent_path}. Restarting...")
                    # Restart the agent in the background
                    subprocess.Popen(
                        [sys.executable, agent_path, "CHIMERA_WAKE"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            
            # Check every 30 seconds
            time.sleep(30)

if __name__ == "__main__":
    # Example: Guarding the Hijacker and the Proxy
    watched = [
        "/home/dan/Chimera_Project/agents/207_MotD_Hijacker/src/main.py",
        "/home/dan/Chimera_Project/agents/302_Pivoting_Proxy/src/main.py"
    ]
    PersistenceWatchdog(watched).monitor_loop()
