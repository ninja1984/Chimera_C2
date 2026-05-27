#!/home/dan/Chimera_Project/venv/bin/python3
import os, sys, re

def manual_forge(repo_path, target_ip, target_port):
    print(f"--- [AGENT 214: REFINED REGEX FOR {target_ip}:{target_port}] ---")
    exploit_file = ""
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.endswith('.py') and 'exploit' in f.lower():
                exploit_file = os.path.join(root, f)
                break
    
    if not exploit_file: return

    with open(exploit_file, 'r') as f:
        code = f.read()

    code = re.sub(r'portFTP\s*=\s*".*?"', f'portFTP = "{target_port}"', code)
    code = re.sub(r'port\s*=\s*\d+', f'port = {target_port}', code)
    code = code.replace('127.0.0.1', target_ip)
    
    output_path = "/home/dan/Chimera_Project/agents/214_Payload_Smithy/loot/forged_exploit.py"
    with open(output_path, 'w') as f:
        f.write(code)
    print(f"[+] FORGE COMPLETE: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 3: manual_forge(sys.argv[1], sys.argv[2], sys.argv[3])
