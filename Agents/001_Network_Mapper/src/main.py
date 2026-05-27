#!/home/dan/Chimera_Project/venv/bin/python3
import subprocess, os, sys, random, socket, time, re

class TacticalMapper:
    """
    Advanced Network Reconnaissance Engine - Division 00 (Recon)
    Implements Low-Level Packet Manipulation, IDS Evasion, and Decoy Arrays.
    """
    def __init__(self, target):
        self.target = target
        self.loot_dir = "/home/dan/Chimera_Project/agents/01_Network_Mapper/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        self.output_file = f"{self.loot_dir}/nmap_{self.target}.txt"
        
        # --- MILITARY GRADE PRIMITIVES ---
        self.source_port = 53        # DNS Masking to bypass egress filters
        self.mtu_size = 8           # Minimal fragments to confuse stateful inspection
        self.data_len = 32          # Random junk data padding to change packet size
        self.max_retries = 1        # Keep noise low to avoid rate-limiting
        self.spoof_mac = "00:11:22:33:44:55"

    def _generate_decoy_flood(self, count=12):
        """Generates a randomized array of decoys to mask the true scanning IP."""
        # Using RND:10 logic to generate random internal-range IPs
        return ",".join([f"10.0.2.{random.randint(5, 254)}" for _ in range(count)])

    def get_tactical_profile(self, profile_name):
        """
        Returns full command-line flag sets for various evasion profiles.
        """
        decoys = self._generate_decoy_flood()
        
        profiles = {
            "GHOST": [
                "-sS", "-Pn", "-f", "--mtu", str(self.mtu_size),
                "-T2", "--data-length", str(self.data_len),
                "-D", f"RND:{random.randint(5,15)}", "-g", str(self.source_port),
                "--randomize-hosts", "--version-intensity", "0",
                "--spoof-mac", "0" # Randomize MAC
            ],
            "SURGICAL": [
                "-sS", "-sV", "-Pn", "-T4", 
                "--version-intensity", "9",
                "--script", "ftp-vsftpd-backdoor,banner,real-vnc-auth-bypass,smb-vuln-ms17-010",
                "-p", "21,2121,80,443,7474,7687,6200,445,3389"
            ],
            "ADAPTIVE": [
                "-sS", "-sV", "-f", "-T3", 
                "--ttl", str(random.randint(64, 128)),
                "--max-retries", str(self.max_retries),
                "--scan-delay", "500ms"
            ]
        }
        return profiles.get(profile_name.upper(), profiles["SURGICAL"])

    def execute(self, profile="SURGICAL"):
        print(f"--- [AGENT 01: TACTICAL RECONNAISSANCE - {self.target}] ---")
        flags = self.get_tactical_profile(profile)
        
        # Binary execution via subprocess with real-time pipe for the Chimera Brain
        cmd = ["nmap"] + flags + [self.target, "-oN", self.output_file]
        
        print(f"[*] ENGAGING PROFILE: {profile}")
        print(f"[*] PRIMITIVES: MTU={self.mtu_size}, SOURCE_PORT={self.source_port}, DATA_LEN={self.data_len}")
        
        if "-D" in flags:
            print(f"[*] DECOY FLOOD: ACTIVE")

        try:
            # We use Popen to monitor the discovery of services in real-time
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            # Stream discovery output for the Brain's immediate analysis
            for line in process.stdout:
                if "Discovered open port" in line or "Scanning" in line:
                    port_match = re.search(r"port (\d+)/tcp", line)
                    if port_match:
                        print(f"    [!] PORT IDENTIFIED: {port_match.group(1)}")
                    else:
                        print(f"    [>] {line.strip()}")
            
            process.wait()
            
            if process.returncode == 0:
                print(f"[+] INTELLIGENCE COMMITTED: {self.output_file}")
                return self.output_file
            else:
                print(f"[!] EXECUTION ERROR: Verify root privileges for raw socket access.")
                return None
                
        except Exception as e:
            print(f"[!!!] FATAL AGENT 01 FAILURE: {e}")
            return None

if __name__ == "__main__":
    # Integration for standalone testing
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    profile_choice = sys.argv[2] if len(sys.argv) > 2 else "SURGICAL"
    
    mapper = TacticalMapper(target_ip)
    mapper.execute(profile_choice)
