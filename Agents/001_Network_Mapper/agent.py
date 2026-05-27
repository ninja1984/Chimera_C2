#!/home/dan/Chimera_Project/venv/bin/python3
import subprocess, os, sys, random, socket, time

class TacticalMapper:
    """
    Advanced Network Reconnaissance Engine - Phase 1 (Reconnaissance)
    Implements low-level packet manipulation and IDS evasion techniques.
    """
    def __init__(self, target):
        self.target = target
        self.loot_dir = "/home/dan/Chimera_Project/agents/01_Network_Mapper/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.output_file = f"{self.loot_dir}/nmap_{self.target}.txt"
        
        # --- MILITARY GRADE CONFIGURATION ---
        self.source_port = 53 # DNS Masking
        self.mtu_size = 8    # Tiny fragments to defeat stateful inspection
        self.data_len = 32   # Random data padding
        self.max_retries = 1 # Minimize noise on failed probes

    def generate_decoy_array(self, count=5):
        """Generates a randomized array of internal IP decoys."""
        return ",".join([f"10.0.2.{random.randint(5, 254)}" for _ in range(count)])

    def get_tactical_flags(self, profile):
        """
        Returns complex flag sets based on established offensive profiles.
        """
        decoys = self.generate_decoy_array()
        
        profiles = {
            "GHOST": [
                "-sS", "-Pn", "-f", "--mtu", str(self.mtu_size),
                "-T2", "--data-length", str(self.data_len),
                "-D", decoys, "-g", str(self.source_port),
                "--randomize-hosts", "--version-intensity", "0"
            ],
            "SURGICAL": [
                "-sS", "-sV", "-Pn", "-T4", 
                "--version-intensity", "9",
                "--script", "ftp-vsftpd-backdoor,banner,real-vnc-auth-bypass",
                "-p", "21,2121,80,443,7474,7687,6200"
            ],
            "ADAPTIVE": [
                "-sS", "-sV", "-f", "-T3", 
                "--ttl", str(random.randint(64, 128)),
                "--max-retries", str(self.max_retries)
            ]
        }
        return profiles.get(profile.upper(), profiles["ADAPTIVE"])

    def execute(self, profile="SURGICAL"):
        print(f"--- [AGENT 01: TACTICAL RECONNAISSANCE - TARGET: {self.target}] ---")
        flags = self.get_tactical_flags(profile)
        
        # Construct the execution command with full primitive control
        cmd = ["nmap"] + flags + [self.target, "-oN", self.output_file]
        
        print(f"[*] ENGAGING PROFILE: {profile}")
        print(f"[*] DECOYS ACTIVE: {flags[flags.index('-D')+1] if '-D' in flags else 'None'}")
        print(f"[*] PACKET MTU: {self.mtu_size} | DATA PADDING: {self.data_len} bytes")

        try:
            # Stream output directly to terminal to monitor for IDS rate-limiting
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            for line in process.stdout:
                if "Scanning" in line or "Discovered" in line:
                    print(f"    [>] {line.strip()}")
            
            process.wait()
            
            if process.returncode == 0:
                print(f"[+] INTELLIGENCE GATHERED: {self.output_file}")
            else:
                error_log = process.stderr.read()
                print(f"[!] KERNEL/SOCKET ERROR: {error_log}")
                
        except Exception as e:
            print(f"[!!!] FATAL AGENT FAILURE: {e}")

if __name__ == "__main__":
    # Ensure usage of venv for library consistency
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    profile_choice = sys.argv[2] if len(sys.argv) > 2 else "SURGICAL"
    
    mapper = TacticalMapper(target_ip)
    mapper.execute(profile_choice)
