#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class ThreadHider:
    """
    Agent 417: Thread Identity Obfuscation.
    Orchestrates C-native thread creation with PR_SET_NAME 
    to blend into the kernel's process accounting.
    """
    def execute(self):
        src = "/home/dan/Chimera_Project/agents/417_Thread_Hider/src/hider.c"
        bin_out = "/home/dan/Chimera_Project/agents/417_Thread_Hider/src/hider"
        
        # Compile with pthread support
        subprocess.run(["gcc", src, "-o", bin_out, "-lpthread"], check=True)
        
        # Execute
        subprocess.run([bin_out])

if __name__ == "__main__":
    ThreadHider().execute()
