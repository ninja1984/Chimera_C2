#!/usr/bin/env python3
import socket, sys

state = {"proxy_active": False, "internal_compromised": False}

def handle_autonomous_command(command):
    cmd_parts = command.strip().split()
    if not cmd_parts: return "[-] Error: Empty command."
    base_cmd = cmd_parts[0].lower()
    
    if base_cmd == "nodes":
        out = "\n--- Active Chimera Nodes ---\n[1] 10.0.2.15 - Status: ALIVE (External DMZ)\n"
        if state["internal_compromised"]: out += "[2] 192.168.1.50 - Status: ALIVE (Internal DC)\n"
        return out + "----------------------------\n"
        
    elif base_cmd == "task":
        if len(cmd_parts) < 3: return "[!] Usage: task <id> <raw bash command>"
        nid = cmd_parts[1]
        task_str = " ".join(cmd_parts[2:])
        if nid == "1":
            if "nmap" in task_str:
                return "[+] Task 'nmap' Output:\nStarting Nmap...\nNmap scan report for 192.168.1.50\nHost is up.\nPORT 445/tcp open"
            return f"[+] Task '{task_str}' Output:\nExecution successful on Node 1."
        elif nid == "2":
            if not state["internal_compromised"]: return "[!] Invalid node ID '2'. Node offline."
            return f"[+] Task '{task_str}' Output:\nExecution successful on Node 2."
        return f"[!] Invalid node ID '{nid}'."

    elif base_cmd == "agent":
        if len(cmd_parts) < 4: return "[!] Usage: agent <id> <local_file> <remote_path>"
        nid, remote_path = cmd_parts[1], cmd_parts[3]
        if nid == "1" or (nid == "2" and state["internal_compromised"]):
            return f"[+] Agent Deployment Status:\nAgent Deployed to {remote_path} and Detached in Background."
        return f"[!] Invalid node ID '{nid}'."

    elif base_cmd == "loot":
        if len(cmd_parts) < 3: return "[!] Usage: loot <id> <filepath>"
        nid, filepath = cmd_parts[1], cmd_parts[2]
        if nid == "2" and "shadow" in filepath:
            return "[+] Extracted File Content:\nroot:$6$exfilmaster...:19842:0:99999:7:::\nMISSION ACCOMPLISHED"
        elif nid == "2":
            return f"[-] Loot failed. File '{filepath}' not found on Node 2. Try looting /etc/shadow."
        return "[-] Loot failed. File not found."
        
    elif base_cmd == "spear":
        if len(cmd_parts) < 2: return "[!] Usage: spear <ip>"
        if cmd_parts[1] == "192.168.1.50":
            state["internal_compromised"] = True
            return "\n[+] GHOST SHELL SECURED: 192.168.1.50 connected as Node 2."
        return "[-] Spear failed: Connection timeout."

    return f"*** Unknown syntax: {command}"

def start_mock_api():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("127.0.0.1", 9999)); s.listen(5)
    print("[*] Mock Hive C2 listening for AI commands on 127.0.0.1:9999\n")
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(4096).decode('utf-8').strip()
            if data: conn.sendall(handle_autonomous_command(data).encode('utf-8'))
            conn.close()
        except: break

if __name__ == "__main__":
    start_mock_api()
