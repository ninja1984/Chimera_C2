#!/usr/bin/env python3
import subprocess
import os
import sys

def map_pivot_potential():
    print("[*] [Agent 50] Pivot-Point-Mapper: Analyzing network interfaces for lateral movement...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "pivot_analysis.txt")
    
    results = []

    # 1. Identify all Network Interfaces
    print("[*] Identifying IP addresses and subnets...")
    try:
        # 'ip addr' gives us the most detail on Linux
        ip_addr_output = subprocess.check_output(["ip", "-o", "addr", "show"], stderr=subprocess.DEVNULL).decode()
        interfaces = []
        for line in ip_addr_output.split('\n'):
            if 'inet ' in line:
                parts = line.split()
                iface = parts[1]
                ip = parts[3]
                interfaces.append(f"{iface}: {ip}")
        
        if len(interfaces) > 2: # More than just lo and one eth
            msg = f"[!] HIGH PIVOT POTENTIAL: Multiple interfaces found: {', '.join(interfaces)}"
            print(msg)
            results.append(msg)
        else:
            results.append(f"Interfaces found: {', '.join(interfaces)}")

    except Exception as e:
        print(f"[!] Error reading interfaces: {e}")

    # 2. Check for Established Internal Connections
    print("[*] Checking active internal connections...")
    try:
        # 'ss' is the modern 'netstat'
        ss_output = subprocess.check_output(["ss", "-nt"], stderr=subprocess.DEVNULL).decode()
        internal_conns = []
        for line in ss_output.split('\n'):
            # Filter for common internal private IP ranges
            if any(x in line for x in ["10.", "192.168.", "172."]):
                internal_conns.append(line.strip())
        
        if internal_conns:
            msg = f"[+] Established internal traffic detected ({len(internal_conns)} connections)."
            print(msg)
            results.append(msg + "\n" + "\n".join(internal_conns))
            
    except Exception as e:
        print(f"[!] Error reading socket stats: {e}")

    with open(loot_path, "w") as f:
        f.write("--- Lateral Movement & Pivot Analysis ---\n")
        if results:
            f.write("\n\n".join(results))
        else:
            f.write("No significant pivot indicators found.")

    print(f"[*] Pivot analysis complete. Results saved to {loot_path}")

if __name__ == "__main__":
    # Local-only execution for post-exploitation intel
    map_pivot_potential()
