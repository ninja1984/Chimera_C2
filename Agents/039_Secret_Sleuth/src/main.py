#!/usr/bin/env python3
import os
import re
import sys

def scan_secrets():
    print("[*] [Agent 32] Secret-Sleuth: Scanning local environment for leaked credentials...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "leaked_secrets.txt")
    
    # Regex patterns for common secrets
    patterns = {
        "AWS_KEY": r"AKIA[0-9A-Z]{16}",
        "AWS_SECRET": r"(['\"]|)(?:AWS_SECRET_ACCESS_KEY|SECRET_KEY)(['\"]|)\s*[:=]\s*(['\"])([A-Za-z0-9/+=]{40})\3",
        "GENERIC_PASS": r"(?:password|passwd|pwd|db_pass)\s*[:=]\s*['\"]?([A-Za-z0-9!@#$%^&*()_+]{6,})['\"]?",
        "SSH_PRIVATE_KEY": r"-----BEGIN (?:RSA|OPENSSH|DSA|EC|PGP) PRIVATE KEY-----"
    }

    found_secrets = []

    # 1. Scan Environment Variables
    for key, value in os.environ.items():
        for name, pattern in patterns.items():
            if re.search(pattern, f"{key}={value}", re.IGNORECASE):
                found_secrets.append(f"[ENV] {name} found in variable: {key}")

    # 2. Scan History Files (Standard Linux)
    history_file = os.path.expanduser("~/.bash_history")
    if os.path.exists(history_file) and os.access(history_file, os.R_OK):
        with open(history_file, 'r', errors='ignore') as f:
            lines = f.readlines()
            for line in lines:
                for name, pattern in patterns.items():
                    if re.search(pattern, line):
                        found_secrets.append(f"[HISTORY] {name} found in .bash_history: {line.strip()}")

    # 3. Check for SSH Keys
    ssh_dir = os.path.expanduser("~/.ssh")
    if os.path.exists(ssh_dir):
        for file in os.listdir(ssh_dir):
            file_path = os.path.join(ssh_dir, file)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if "-----BEGIN" in content:
                            found_secrets.append(f"[FILES] SSH Private Key found: {file_path}")
                except:
                    continue

    with open(loot_path, "w") as f:
        f.write("--- Local Secret Discovery Report ---\n")
        if found_secrets:
            for secret in set(found_secrets): # Unique results only
                print(f"[!] {secret}")
                f.write(secret + "\n")
        else:
            f.write("No obvious secrets found in local environment or history.")

    print(f"[*] Scan complete. Results saved to {loot_path}")

if __name__ == "__main__":
    scan_secrets()
