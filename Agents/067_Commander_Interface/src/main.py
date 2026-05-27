import subprocess
import os
import sys
import time

class ChimeraCommander:
    """
    Chimera Agent 60: The Orchestrator (V6.0 - COMPLETE GHOST CHAIN)
    Purpose: End-to-end automation from Recon to Remote Exfiltration.
    """
    def __init__(self):
        self.script_path = os.path.abspath(__file__)
        self.agents_dir = os.path.dirname(os.path.dirname(os.path.dirname(self.script_path)))
        self.intel_file = os.path.join(self.agents_dir, "master_intel.json")

    def run_agent(self, prefix, args=""):
        """Helper to run an agent by its number prefix."""
        for entry in os.listdir(self.agents_dir):
            if entry.startswith(f"{prefix}_"):
                script = os.path.join(self.agents_dir, entry, "src", "main.py")
                if os.path.exists(script):
                    print(f"\n[>>>] COMMANDER: Launching Agent {entry}...")
                    # Using os.system for interactive TTY handover
                    cmd = f"{sys.executable} {script} {args}"
                    exit_code = os.system(cmd)
                    return exit_code == 0
        print(f"[!] Agent {prefix} not found.")
        return False

    def execute_full_chain(self):
        """
        THE 'GHOST' SEQUENCE:
        01 Mapper -> 14 Parser -> 66 Sprayer -> 70 Zipper -> 71 Uploader -> 22 Poisoner
        """
        print("\n" + "!"*60)
        print("   CHIMERA FULL-CHAIN AUTOMATION :: GHOST SEQUENCE")
        print("!"*60)
        
        steps = [
            ("01", "Network Mapping"),
            ("14", "Intelligence Parsing"),
            ("66", "Credential Spraying"),
            ("70", "Loot Compression"),
            ("71", "Remote Exfiltration"),
            ("22", "Log Sanitization")
        ]

        for i, (prefix, desc) in enumerate(steps, 1):
            print(f"\n[STEP {i}/{len(steps)}] Initiating {desc}...")
            if not self.run_agent(prefix):
                print(f"[!] Chain interrupted at Step {i} (Agent {prefix}).")
                input("Press Enter to attempt to continue, or Ctrl+C to abort...")
            time.sleep(1) 

        print("\n" + "="*60)
        print("   [!!!] MISSION COMPLETE: DATA SECURED AND WIPED [!!!]")
        print("="*60)

    def run(self):
        while True:
            print("\n" + "="*60)
            print("   PROJECT CHIMERA :: COMMANDER v6.0")
            print("="*60)
            print("[01] Mapper    [14] Parser    [66] Sprayer")
            print("[70] Zipper    [71] Uploader  [22] Poisoner")
            print("-" * 60)
            print("[F]  EXECUTE FULL GHOST CHAIN")
            print("[Q]  SHUTDOWN")
            
            choice = input("\nSelect Action > ").strip().lower()

            if choice == 'f':
                self.execute_full_chain()
            elif choice == 'q':
                sys.exit(0)
            elif choice.isdigit():
                self.run_agent(choice.zfill(2))
            else:
                print("[!] Invalid Selection.")

if __name__ == "__main__":
    commander = ChimeraCommander()
    commander.run()
