#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class HookDetector:
    """
    Agent 415: Runtime Integrity Guard.
    Compiles and executes the C-native detector to identify 
    inline API hooks placed by EDR/AV solutions.
    """
    def execute(self):
        src = "/home/dan/Chimera_Project/agents/415_Hook_Detector/src/detector.c"
        bin_out = "/home/dan/Chimera_Project/agents/415_Hook_Detector/src/detector"
        
        # Compile with dl library linked
        subprocess.run(["gcc", src, "-o", bin_out, "-ldl"], check=True)
        
        # Execute the audit
        subprocess.run([bin_out])

if __name__ == "__main__":
    HookDetector().execute()
