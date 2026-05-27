import os
import subprocess
import time
import sys

class ChimeraWatchdog:
    """
    Chimera Agent 88: The Watchdog
    Purpose: Monitor and maintain swarm uptime.
    """
    def __init__(self, targets=["60_Commander_Interface", "93_Persistence_Daemon"]):
        self.targets = targets

    def is_running(self, agent_name):
        """Checks if a specific agent process is active."""
        try:
            cmd = f"ps aux | grep {agent_name} | grep -v grep"
            output = subprocess.check_output(cmd, shell=True)
            return len(output) > 0
        except:
            return False

    def revive(self, agent_name):
        """Restarts the dead agent."""
        print(f"[!] Agent 88: {agent_name} is down. Reviving...")
        # Path logic assumes standard Chimera structure
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), agent_name, "src", "main.py")
        subprocess.Popen([sys.executable, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def run(self):
        print("[*] Agent 88: Watchdog active. Monitoring swarm vitals...")
        while True:
            for target in self.targets:
                if not self.is_running(target):
                    self.revive(target)
            time.sleep(10) # 10-second heartbeat

if __name__ == "__main__":
    watchdog = ChimeraWatchdog()
    watchdog.run()
