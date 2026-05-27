#!/usr/bin/env python3
import os

def profile_users():
    print("[*] [Agent 86] User-Profiler: Extracting user intelligence...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "user_profile.txt")
    
    results = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if int(parts[2]) >= 1000 or int(parts[2]) == 0:
                results.append(f"User: {parts[0]} | UID: {parts[2]} | Shell: {parts[6]}")

    with open(loot_path, "w") as f:
        f.write("\n".join(results))
    print(f"[*] Results saved to {loot_path}")

if __name__ == "__main__":
    profile_users()
