import os
import shutil
import sys

class ScorchedEarth:
    """
    Chimera Agent 114: Scorched Earth
    Purpose: Total forensic destruction of the Chimera Swarm.
    """
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def execute(self):
        print("!!! WARNING: SCORCHED EARTH PROTOCOL INITIATED !!!")
        confirm = input("Confirm total destruction of Project Chimera? (y/n): ")
        
        if confirm.lower() == 'y':
            print("[*] Shreddng loot and logs...")
            # In a military-grade version, we'd overwrite with zeros here.
            try:
                shutil.rmtree(self.root_dir)
                print("[+] Project Chimera has been erased.")
                sys.exit(0)
            except Exception as e:
                print(f"[!] Wipe failed: {e}")
        else:
            print("[-] Protocol aborted.")

if __name__ == "__main__":
    nuke = ScorchedEarth()
    nuke.execute()
