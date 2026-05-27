import os
import sys
import base64
from cryptography.fernet import Fernet

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def get_or_create_key():
    """Manages the Master Encryption Key for the Swarm."""
    key_path = "/home/dan/Chimera_Project/core/.master.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[32m" + "="*60)
    print("   CHIMERA AGENT 53 :: SECURE CREDENTIAL STASHER")
    print("="*60 + "\033[0m")

    # Load Encryption Key
    master_key = get_or_create_key()
    cipher_suite = Fernet(master_key)

    print("[*] Monitoring Neo4j for unencrypted 'Loot' nodes...")
    
    # Logic: Find nodes where 'status' is 'plaintext'
    # For this manual run, we'll take direct input to demonstrate
    raw_user = input("[?] Target Username: ").strip()
    raw_pass = input("[?] Target Password: ").strip()
    target_host = input("[?] Target Host: ").strip()

    # 1. Encrypt the data
    encrypted_pass = cipher_suite.encrypt(raw_pass.encode()).decode()

    print(f"[*] Encrypting credentials for {raw_user}@{target_host}...")

    # 2. Update the Graph
    # We store the encrypted string and mark the node as 'STASHED'
    db.report_finding("53_Credential_Stasher", "Encrypted_Credential_Stored", {
        "host": target_host,
        "user": raw_user,
        "secret_blob": encrypted_pass,
        "security_level": "ENCRYPTED"
    })

    print("\033[92m[+] SUCCESS: Credentials stashed in Neo4j Vault.\033[0m")
    print("[!] Tactical Note: Plaintext source should now be 'rm -rf'ed.")

    db.close()

if __name__ == "__main__":
    run()
