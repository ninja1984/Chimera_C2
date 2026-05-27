#!/usr/bin/env python3
import socket
import re
import json
import urllib.request
import time

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"
ALLOWED_COMMANDS = ['nodes', 'spear', 'proxy', 'loot']

def send_to_hive(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9999))
        s.sendall(command.encode('utf-8'))
        response = s.recv(4096).decode('utf-8')
        s.close()
        return response
    except Exception as e:
        return f"[-] FATAL: Hive API Error - {e}"

def ask_ai(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1} # Low temp for strict logic
    }
    req = urllib.request.Request(OLLAMA_API, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get("response", "")
    except Exception as e:
        return f"THOUGHT: API Error. ACTION: error"

def run_react_loop():
    print(f"[*] Chimera Tactical Engine: Autonomous Handler Online.")
    print(f"[*] Attached to Local Engine: {MODEL_NAME}")
    
    # The System Prompt forces the AI into the ReAct format
    system_context = """
You are the Chimera Tactical AI. Your goal is to enumerate the active targets.
You must strictly use this format:
THOUGHT: [Your reasoning]
ACTION: [A single command]

You are only allowed to use one of these commands: nodes, spear <ip>, proxy <ip>, loot <id> <file>.
If you need to see what is connected, output: ACTION: nodes
"""
    
    print("\n[*] Sending environmental state to AI...")
    raw_ai_output = ask_ai(system_context + "\nWhat is your first move?")
    
    print("\n\033[1;34m[AI OUTPUT]\033[0m")
    print(raw_ai_output.strip())
    print("\033[1;34m--------------------------------------------------\033[0m\n")
    
    # --- PHASE 3: THE SANDBOX CONSTRAINT ---
    match = re.search(r"ACTION:\s*(.*)", raw_ai_output, re.IGNORECASE)
    if not match:
        print("\033[1;33m[-] Sandbox Intercept: AI failed to output a valid ACTION tag. Halting loop.\033[0m")
        return
        
    raw_command = match.group(1).strip()
    base_command = raw_command.split()[0].lower()
    
    if base_command not in ALLOWED_COMMANDS:
        print(f"\033[1;31m[-] Sandbox Intercept: AI attempted unauthorized command '{base_command}'.\033[0m")
        print("[*] The Hive API has been protected. AI hallucination contained.")
        return
        
    print(f"[*] Handler parsed valid action: '{raw_command}'. Piping to Hive API...")
    
    # Execute against the Hive
    result = send_to_hive(raw_command)
    
    print(f"\n[*] Hive C2 Response Received:")
    print("\033[1;32m" + result.strip() + "\033[0m")
    print("\n[*] Agentic Loop Complete.")

if __name__ == "__main__":
    run_react_loop()
