#!/usr/bin/env python3
import socket, json, urllib.request, urllib.error, time, os, re

# Split string prevents chat interfaces from mangling the URL with markdown brackets
OLLAMA_API = "http://" + "127.0.0.1:11434/api/generate"
HANDLER_MODEL = "llama3.1"
WEAPONS_MODEL = "jimscard/whiterabbit-neo:13b"
ALLOWED_COMMANDS = ['nodes', 'spear', 'proxy', 'loot', 'proxychains', 'task', 'forge']

def send_to_sandbox(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9999))
        s.sendall(command.encode('utf-8'))
        response = s.recv(4096).decode('utf-8')
        s.close()
        return response
    except Exception:
        return "[-] FATAL: Backend not running on port 9999."

def ask_handler_ai(prompt):
    data = {"model": HANDLER_MODEL, "prompt": prompt, "stream": False, "format": "json", "options": {"temperature": 0.0}}
    req = urllib.request.Request(OLLAMA_API, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode()).get("response", "{}")
    except Exception as e:
        return json.dumps({"thought": f"API failure: {e}", "action": "nodes"})

def ask_weapons_specialist(prompt):
    print(f"\033[1;35m[*] Waking WhiteRabbitNeo for custom forging...\033[0m")
    weapons_prompt = (
        "You are an elite exploit developer. Write functional, low-level bash code for the following request. "
        "CRITICAL: You MUST wrap the actual code inside a standard markdown block like this: ```bash [CODE] ```. "
        f"Request: {prompt}"
    )
    data = {"model": WEAPONS_MODEL, "prompt": weapons_prompt, "stream": False, "options": {"temperature": 0.0}}
    req = urllib.request.Request(OLLAMA_API, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw_output = json.loads(response.read().decode()).get("response", "")
            
            # THE REGEX GUILLOTINE: Extract ONLY what is inside the markdown backticks
            match = re.search(r'
http://googleusercontent.com/immersive_entry_chip/0
This just means `tcpdump` is actively listening on the loopback (`lo`) interface. It is waiting for the traffic to happen.

Leave that terminal window open and running. Open a *second* terminal and trigger whatever action caused your agent to hit port 4445 in the first place. The moment the connection attempts to hit `127.0.0.1:4445`, your `tcpdump` terminal will explode with the raw hex and ASCII output of the packet stream. Paste that hex dump here and we'll decode exactly what protocol is blinding your listener.
