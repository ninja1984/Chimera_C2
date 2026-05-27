import os
import sys
import requests
import re

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[36m" + "="*60)
    print("   CHIMERA AGENT 24 :: JOOMLA RECON (CRASH-PROOF)")
    print("="*60 + "\033[0m")

    target = input("[?] Target URL (e.g. http://10.0.2.5/joomla): ").strip()
    if not target.startswith("http"):
        target = f"http://{target}"

    # 0. Initial Alive Check
    try:
        requests.get(target, timeout=3)
    except Exception:
        print(f"\033[91m[!] Target {target} is unreachable. Is the web server running?\033[0m")
        return

    print(f"[*] Scanning {target} for Joomla signatures...")

    # 1. Version Detection
    manifest_url = f"{target}/administrator/manifests/files/joomla.xml"
    try:
        r = requests.get(manifest_url, timeout=5)
        version = re.search(r"<version>(.*?)</version>", r.text)
        if version:
            v_num = version.group(1)
            print(f"\033[92m[+] Found Joomla Version: {v_num}\033[0m")
            db.report_finding("24_Joomla_Scanner", "CMS_Version", {"software": "Joomla", "version": v_num, "target": target})
    except:
        pass

    # 2. User Enumeration
    print("[*] Attempting User Enumeration...")
    try:
        r = requests.get(target, timeout=5)
        found_users = re.findall(r"/author/(.*?)\"", r.text)
        if found_users:
            for u in set(found_users):
                print(f"\033[94m[+] Discovered User: {u}\033[0m")
                db.report_finding("24_Joomla_Scanner", "User_Enumerated", {"user": u, "target": target})
    except:
        pass

    # 3. Critical Path Check (Now wrapped in try/except)
    paths = ["/administrator/", "/bin/joomla.xml", "/configuration.php-dist"]
    for p in paths:
        try:
            res = requests.get(target + p, timeout=3)
            if res.status_code == 200:
                print(f"\033[93m[!] Exposed Path: {p}\033[0m")
                db.report_finding("24_Joomla_Scanner", "Exposed_Path", {"path": p, "target": target})
        except requests.exceptions.RequestException:
            continue

    print("\n[*] Scan complete.")
    db.close()

if __name__ == "__main__":
    run()
