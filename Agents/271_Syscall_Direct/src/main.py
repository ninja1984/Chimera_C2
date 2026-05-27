#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class SyscallDirect:
    """
    Agent 416: Kernel Direct-Interface & Signal Recovery.
    Compiles the C-native bypass to ensure Chimera can talk to the 
    kernel even when the user-land environment is heavily hooked.
    """
    def execute(self):
        src = "/home/dan/Chimera_Project/agents/416_Syscall_Direct/src/bypass.c"
        bin_out = "/home/dan/Chimera_Project/agents/416_Syscall_Direct/src/bypass"
        
        # Compile the bypass
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Execute
        subprocess.run([bin_out])

if __name__ == "__main__":
    SyscallDirect().execute()
