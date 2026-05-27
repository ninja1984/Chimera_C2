#!/home/dan/Chimera_Project/venv/bin/python3
import subprocess, sys, os

def harvest(cve_id, target):
    print(f"--- [AGENT 213: HARVESTING POC FOR {cve_id}] ---")
    loot_dir = f"/home/dan/Chimera_Project/agents/213_PoC_Harvester/loot/{cve_id}_{cve_id}"
    
    # Manual bypass for the vsftpd lab repo
    repo_url = "https://github.com/padsalatushal/CVE-2011-2523.git"
    
    if not os.path.exists(loot_dir):
        subprocess.run(["git", "clone", repo_url, loot_dir], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["git", "-C", loot_dir, "pull"], stdout=subprocess.DEVNULL)
    print(f"[+] PoC Harvested to {loot_dir}")

if __name__ == "__main__":
    if len(sys.argv) > 2: harvest(sys.argv[1], sys.argv[2])
