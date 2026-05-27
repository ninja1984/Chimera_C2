#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
from datetime import datetime, timedelta

class LogicBomb:
    """
    Agent 215: Dead-Man's Switch & Logic Trigger.
    Monitors for a 'Stay-Alive' signal. If the signal is missed, 
    it executes a pre-defined contingency command (Wipe or Lock).
    """
    def __init__(self, trigger_cmd, delay_minutes=60):
        self.trigger_cmd = trigger_cmd
        self.delay = delay_minutes
        self.check_in_file = "/tmp/.sys-heartbeat"
        # Set the initial 'Dead-Man' timer
        self.reset_timer()

    def reset_timer(self):
        """Updates the heartbeat file to 'Postpone' the bomb."""
        with open(self.check_in_file, 'w') as f:
            # Write the timestamp when the bomb SHOULD go off
            expiry = datetime.now() + timedelta(minutes=self.delay)
            f.write(expiry.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"[*] Timer Reset. Next trigger at: {expiry}")

    def monitor(self):
        print(f"--- [AGENT 215: LOGIC BOMB ACTIVE] ---")
        
        # Fork to background
        if os.fork() > 0: sys.exit(0)

        while True:
            if not os.path.exists(self.check_in_file):
                # If the file is deleted, it means we lost control. TRIGGER.
                os.system(self.trigger_cmd)
                break

            with open(self.check_in_file, 'r') as f:
                try:
                    expiry_str = f.read().strip()
                    expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
                    
                    if datetime.now() > expiry_dt:
                        print("[!!!] TIMER EXPIRED. EXECUTING CONTINGENCY.")
                        os.system(self.trigger_cmd)
                        # Self-destruct the bomb agent after execution
                        os.remove(self.check_in_file)
                        break
                except Exception:
                    pass
            
            # Check every minute
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py '<contingency_command>' [delay_mins]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    mins = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    # Example: ./main.py 'python3 /path/to/agent_212/src/main.py' 120
    LogicBomb(cmd, mins).monitor()
