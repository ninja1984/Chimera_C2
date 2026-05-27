#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class ProcessMigratorHardened:
    """
    Agent 413: C-Native Process Injection Runner.
    Compiles the low-level ptrace injector and targets a 
    trusted system PID for ghost residency.
    """
    def execute(self, target_pid):
        print(f"--- [AGENT 413: C-NATIVE MIGRATION ACTIVE] ---")
        src = "/home/dan/Chimera_Project/agents/413_Process_Migrator/src/injector.c"
        bin_out = "/home/dan/Chimera_Project/agents/413_Process_Migrator/src/injector"
        
        # Compile the injector
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Run as Root (Required for ptrace on other processes)
        if os.getuid() != 0:
            print("[!] Critical: Migration requires Root/CAP_SYS_PTRACE.")
            return

        subprocess.run([bin_out, str(target_pid)])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_pid>")
        sys.exit(1)
    ProcessMigratorHardened().execute(sys.argv[1])
