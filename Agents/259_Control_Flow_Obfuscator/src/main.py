#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class ControlFlowObfuscator:
    """
    Agent 404: Static Analysis Disrupter.
    Wraps Chimera primitives in complex C-based 'Opaque Predicates' 
    to break decompiler logic and slow down manual reverse engineering.
    """
    def __init__(self):
        self.src = "/home/dan/Chimera_Project/agents/404_Control_Flow_Obfuscator/src/obfuscator.c"
        self.bin = "/home/dan/Chimera_Project/agents/404_Control_Flow_Obfuscator/src/chimera_obf"

    def execute(self):
        print("--- [AGENT 404: CONTROL FLOW OBFUSCATION] ---")
        
        # Compile with -O0 to prevent GCC from optimizing away the 'Dead Code'
        # We WANT the junk code to stay in the binary to confuse Ghidra.
        print("[*] Compiling with Anti-Disassembly primitives...")
        try:
            subprocess.run(["gcc", "-O0", self.src, "-o", self.bin], check=True)
            print(f"[!!!] SUCCESS: Obfuscated binary created at {self.bin}")
        except Exception as e:
            print(f"[!] Compilation failed: {e}")

if __name__ == "__main__":
    ControlFlowObfuscator().execute()
