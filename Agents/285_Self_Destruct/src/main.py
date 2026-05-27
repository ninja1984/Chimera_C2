#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class HardenedSelfDestruct:
    """
    Agent 430 (Hardened): C-Native Anti-Forensic Purge.
    Compiles and executes the memory-scrubbing primitive to 
    ensure zero-trace residency and secure termination.
    """
    def execute(self):
        print("--- [AGENT 430: HARDENED SELF-DESTRUCT ACTIVE] ---")
        src = "/home/dan/Chimera_Project/agents/430_Self_Destruct/src/purge.c"
        bin_out = "/home/dan/Chimera_Project/agents/430_Self_Destruct/src/purge"
        
        # Compile the purge primitive
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Execute the purge
        subprocess.run([bin_out])

if __name__ == "__main__":
    HardenedSelfDestruct().execute()
