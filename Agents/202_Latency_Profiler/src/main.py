#!/usr/bin/env python3
import socket
import time
import sys
import os

def profile_latency(target_host, port=80):
    print(f"[*] [Agent 189] Latency-Profiler: Profiling {target_host}:{port}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "latency_report.txt")
    
    if not os.path.exists(os.path.dirname(loot_path)):
        os.makedirs(os.path.dirname(loot_path))

    latencies = []
    
    print("[*] Performing 5-step timing analysis...")
    for i in range(5):
        try:
            start_time = time.perf_counter()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            # Measuring the time it takes to complete the 3-way handshake
            sock.connect((target_host, port))
            
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000 # Convert to ms
            latencies.append(duration)
            print(f"    [+] Sample {i+1}: {duration:.2f}ms")
            sock.close()
            time.sleep(1) # Stealth delay
        except Exception as e:
            print(f"    [!] Sample {i+1} Failed: {e}")

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        result_str = f"Target: {target_host}\nAverage TCP Handshake Latency: {avg_latency:.2f}ms\nSamples: {latencies}\n"
        
        with open(loot_path, "w") as f:
            f.write(result_str)
        print(f"[+] Average Latency: {avg_latency:.2f}ms. Report saved.")
    else:
        print("[!] Profiling failed. No data collected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_host> [port]")
        sys.exit(1)
    
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    profile_latency(sys.argv[1], port)
