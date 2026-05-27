#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class MemoryWiperHardened:
    """
    Agent 405: C-Native Implementation.
    Compiles and executes the memory-pinned guard to 
    ensure zero-leakage during forensic imaging.
    """
    def execute(self):
        print("--- [AGENT 405: HARDENED C-GUARD START] ---")
        src = "/home/dan/Chimera_Project/agents/405_Memory_Wiper/src/wiper.c"
        bin_out = "/home/dan/Chimera_Project/agents/405_Memory_Wiper/src/wiper"
        
        # Compile with -O0 to be extra safe against optimization
        subprocess.run(["gcc", "-O0", src, "-o", bin_out], check=True)
        
        # Run it (Requires sudo/root for mlock in some environments)
        subprocess.run([bin_out])

if __name__ == "__main__":
    MemoryWiperHardened().execute()
