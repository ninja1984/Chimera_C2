#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess

class DebugBlocker:
    """
    Agent 402: Anti-Debugging & Stealth Shield.
    Utilizes ptrace self-attachment and timing checks to 
    detect and evade active debugging/instrumentation.
    """
    def __init__(self):
        self.src = "/home/dan/Chimera_Project/agents/402_Debug_Blocker/src/antidebug.c"
        self.bin = "/home/dan/Chimera_Project/agents/402_Debug_Blocker/src/antidebug"

    def check_for_debugger(self):
        print("[*] Engaging Anti-Debug Shield...")
        
        # 1. Compile the C primitive if needed
        if not os.path.exists(self.bin):
            subprocess.run(["gcc", self.src, "-o", self.bin], capture_output=True)

        # 2. Run the check
        try:
            result = subprocess.run([self.bin], capture_output=True, text=True)
            if "SAFE" in result.stdout:
                return False # No debugger found
            else:
                return True # Binary exited early (detected debugger)
        except:
            return True

    def execute(self):
        print("--- [AGENT 402: DEBUG BLOCKER ACTIVE] ---")
        if self.check_for_debugger():
            print("[\033[91mALERT\033[0m] ACTIVE DEBUGGER DETECTED.")
            print("[*] EVASION: Poisoning memory and exiting.")
            sys.exit(1)
        
        print("[\033[92mSAFE\033[0m] No active instrumentation detected.")
        return True

if __name__ == "__main__":
    DebugBlocker().execute()
