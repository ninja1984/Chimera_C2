#!/usr/bin/env python3
import subprocess
import os
import sys

def notify_neighbors():
    print("[*] [Agent 193] Neighbor-Notifier: Extracting network topology...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "neighbor_report.txt")
    
    results = []

    # 1. Extract ARP Cache (Neighbors the OS has talked to recently)
    results.append("--- ARP CACHE (Local Neighbors) ---")
    try:
        arp_data = subprocess.check_output(["ip", "neigh", "show"], stderr=subprocess.DEVNULL).decode().strip()
        results.append(arp_data if arp_data else "No neighbors in ARP cache.")
    except Exception as e:
        results.append(f"Error reading ARP: {e}")

    results.append("\n--- ROUTING TABLE (Network Pathing) ---")
    # 2. Extract Routing Table (Where the traffic goes)
    try:
        route_data = subprocess.check_output(["ip", "route", "show"], stderr=subprocess.DEVNULL).decode().strip()
        results.append(route_data if route_data else "No routes defined.")
    except Exception as e:
        results.append(f"Error reading Routes: {e}")

    # Write findings to loot
    with open(loot_path, "w") as f:
        f.write("\n".join(results))
    
    print(f"[+] Passive discovery complete. Results saved to {loot_path}")

if __name__ == "__main__":
    notify_neighbors()
