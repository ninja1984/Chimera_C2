import os
import sys
import subprocess
import time

class SUIDSearcher:
    """
    Chimera Agent 20: SUID Searcher (GTFOBins Integrated)
    Purpose: Identify SUID binaries and cross-reference with known exploits.
    """
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.agent_root = os.path.dirname(self.script_dir)
        self.loot_dir = os.path.join(self.agent_root, "loot")
        
        # High-probability GTFOBins targets (Local Cache)
        self.gtfo_list = [
            "awk", "base64", "bash", "cp", "cpulimit", "curl", "dash", "dd", 
            "docker", "ed", "env", "expand", "expect", "find", "flock", "fmt", 
            "fold", "gdb", "gimp", "grep", "head", "ionice", "ip", "journalctl", 
            "jq", "jjs", "ksh", "ld.so", "less", "lwp-download", "make", "more", 
            "mv", "nano", "nmap", "node", "od", "openssl", "perl", "php", "python", 
            "readelf", "restic", "rvim", "sed", "sh", "socat", "sort", "sqlite3", 
            "ssh-keygen", "stdbuf", "strace", "systemctl", "tail", "tar", "tee", 
            "telnet", "tclsh", "time", "timeout", "ul", "unexpand", "vim", "watch", 
            "wget", "xargs", "xxd", "zip", "zsh"
        ]

    def log_match(self, bin_path, bin_name):
        """Logs the exploitable binary to the loot folder."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_file = os.path.join(self.loot_dir, f"exploit_targets_{timestamp}.txt")
        
        # Construct the GTFOBins URL for quick reference
        gtfo_url = f"https://gtfobins.github.io/gtfobins/{bin_name}/#suid"
        
        with open(log_file, "a") as f:
            f.write(f"[!!!] POTENTIAL EXPLOIT FOUND: {bin_path}\n")
            f.write(f"      Reference: {gtfo_url}\n")
            f.write("-" * 50 + "\n")

    def run_scan(self):
        print("\n[*] Agent 20: Commencing SUID scan (Root-owned)...")
        # Standard find command for SUID binaries owned by root
        cmd = "find / -perm -4000 -user root -type f 2>/dev/null"
        
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            binaries = output.strip().split('\n')
            
            print(f"[*] Found {len(binaries)} SUID binaries. Cross-referencing...")
            
            matches = 0
            for bin_path in binaries:
                bin_name = os.path.basename(bin_path)
                if bin_name in self.gtfo_list:
                    print(f"\n[!!!] MATCH: {bin_name} is in GTFOBins! ({bin_path})")
                    print(f"      Visit: https://gtfobins.github.io/gtfobins/{bin_name}/#suid")
                    self.log_match(bin_path, bin_name)
                    matches += 1
            
            if matches == 0:
                print("\n[-] Agent 20: No high-probability GTFO binaries found.")
            else:
                print(f"\n[*] Agent 20: {matches} exploitable binaries logged to loot.")
                
        except Exception as e:
            print(f"[!] Agent 20 Error: {e}")

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 20 :: SUID SEARCHER :: CHIMERA SWARM")
        print("="*60)
        print("1. Run Standard SUID Scan & GTFO Cross-Ref")
        print("2. Update GTFO Cache (Manual List View)")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            self.run_scan()
        elif choice == "2":
            print("\nCurrently Cached GTFO Binaries:")
            print(", ".join(self.gtfo_list))
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    agent = SUIDSearcher()
    agent.menu()
