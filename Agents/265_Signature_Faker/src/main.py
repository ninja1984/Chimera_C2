#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess
import shutil

class SignatureFaker:
    """
    Agent 410: Binary Metadata & Capability Forger.
    Clones the ELF headers, extended attributes, and Linux 
    capabilities of a 'Trusted' binary onto a Chimera agent.
    """
    def __init__(self, target_agent, reference_binary="/bin/ls"):
        self.target = target_agent
        self.reference = reference_binary

    def clone_metadata(self):
        print(f"--- [AGENT 410: DEEP SIGNATURE FORGERY] ---")
        if not os.path.exists(self.reference):
            print(f"[!] Reference {self.reference} not found. Aborting.")
            return

        print(f"[*] Extracting DNA from {self.reference}...")
        
        try:
            # 1. Clone File Ownership and Permissions (Standard)
            shutil.copymode(self.reference, self.target)
            ref_stat = os.stat(self.reference)
            os.chown(self.target, ref_stat.st_uid, ref_stat.st_gid)

            # 2. Clone Linux Capabilities (Military Grade)
            # This is what 'getcap' and 'setcap' use. 
            # If 'ping' has CAP_NET_RAW, our agent will too.
            caps = subprocess.getoutput(f"getcap {self.reference}").split(' = ')
            if len(caps) > 1:
                cap_val = caps[1].strip()
                subprocess.run(["setcap", f"{cap_val}", self.target], capture_output=True)
                print(f"[+] Cloned Capabilities: {cap_val}")

            # 3. Clone Extended Attributes (xattrs)
            # Forensic tools check these for 'Immutable' or 'Security' flags.
            xattrs = subprocess.getoutput(f"getfattr -d {self.reference}").splitlines()
            for line in xattrs:
                if "=" in line and not line.startswith("#"):
                    attr = line.split("=")[0].strip()
                    subprocess.run(["setfattr", "-n", attr, "-v", "...", self.target], capture_output=True)

            print(f"[\033[92mSUCCESS\033[0m] {self.target} is now a 'Twin' of {self.reference}")
            
        except Exception as e:
            print(f"[!] Forgery failed: {e}")

    def execute(self):
        self.clone_metadata()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <agent_path> [reference_path]")
        sys.exit(1)
    
    agent = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 else "/bin/ls"
    SignatureFaker(agent, ref).execute()
