import http.client
import sys
import os
import time

def test_evasion_threshold(target_host):
    """
    Sends varying levels of 'suspicious' payloads to test WAF/IDS sensitivity.
    """
    print(f"[*] [Agent 198] Evasion-Expert: Testing defense thresholds for {target_host}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    loot_path = os.path.join(script_dir, "..", "loot", "waf_sensitivity.txt")

    # Payload levels: Level 1 (Quiet) to Level 4 (Noisy/Obvious)
    test_payloads = [
        {"level": 1, "desc": "Standard Header", "header": {"User-Agent": "Mozilla/5.0"}},
        {"level": 2, "desc": "Custom Header", "header": {"X-Forwarded-For": "127.0.0.1"}},
        {"level": 3, "desc": "Basic SQLi Probe", "header": {"User-Agent": "' OR 1=1--"}},
        {"level": 4, "desc": "Path Traversal Probe", "header": {"User-Agent": "../../../etc/passwd"}}
    ]

    results = []
    conn = http.client.HTTPSConnection(target_host, timeout=5)

    for payload in test_payloads:
        try:
            print(f"[*] Testing Level {payload['level']}: {payload['desc']}...")
            conn.request("GET", "/", headers=payload['header'])
            res = conn.getresponse()
            
            # If we get a 403 Forbidden or a 406 Not Acceptable, the WAF is triggered
            status = res.status
            if status in [403, 406, 501]:
                print(f"[!] Level {payload['level']} BLOCKED (Status: {status})")
                results.append(f"LEVEL_{payload['level']}_BLOCKED: {payload['desc']}")
            else:
                print(f"[+] Level {payload['level']} PASSED (Status: {status})")
                results.append(f"LEVEL_{payload['level']}_PASSED: {payload['desc']}")
            
            res.read() # Clear buffer
            time.sleep(1) # Gentle interval to avoid volumetric triggers
        except Exception as e:
            print(f"[!] Connection failed at Level {payload['level']}: {e}")
            break

    # Save logic for the Commander to read
    if not os.path.exists(os.path.dirname(loot_path)):
        os.makedirs(os.path.dirname(loot_path))
    with open(loot_path, "w") as f:
        for r in results:
            f.write(f"{r}\n")
    
    conn.close()
    print(f"[*] Evasion audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_host>")
        sys.exit(1)
    
    test_evasion_threshold(sys.argv[1])
