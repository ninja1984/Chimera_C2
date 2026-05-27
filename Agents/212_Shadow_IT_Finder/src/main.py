import socket
import sys
import os
import threading

def probe_neighbor(ip, results):
    """
    Performs a low-level TCP connect probe to see if a neighbor is alive.
    """
    try:
        # Testing port 80/443/22 as 'heartbeat' ports
        for port in [80, 443, 22]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    print(f"[+] Shadow-IT Found: {ip} is ALIVE (Port {port})")
                    results.append(ip)
                    return
    except:
        pass

def run_shadow_finder(target_ip):
    print(f"[*] [Agent 199] Shadow-IT-Finder: Scanning neighbors of {target_ip}...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    loot_path = os.path.join(script_dir, "..", "loot", "neighbor_hosts.txt")
    
    # Calculate a small /24 range footprint (neighboring IPs)
    base_ip = ".".join(target_ip.split(".")[:-1])
    current_last_octet = int(target_ip.split(".")[-1])
    
    threads = []
    found_hosts = []

    # Probing +/- 5 neighbors for a tight 'Project Chimera' audit footprint
    for i in range(max(1, current_last_octet - 5), min(255, current_last_octet + 5)):
        if i == current_last_octet: continue
        ip_to_test = f"{base_ip}.{i}"
        t = threading.Thread(target=probe_neighbor, args=(ip_to_test, found_hosts))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if found_hosts:
        if not os.path.exists(os.path.dirname(loot_path)):
            os.makedirs(os.path.dirname(loot_path))
        with open(loot_path, "a") as f:
            for host in found_hosts:
                f.write(f"{host}\n")
        print(f"[*] Shadow-IT audit complete. {len(found_hosts)} neighbors identified.")
    else:
        print("[*] No active neighbors found in immediate proximity.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_ip>")
        sys.exit(1)
    
    run_shadow_finder(sys.argv[1])
