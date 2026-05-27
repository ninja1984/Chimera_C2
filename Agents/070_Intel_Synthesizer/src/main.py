import os
import sys
import requests

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[95m" + "="*60)
    print("   CHIMERA AGENT 63 :: INTEL_SYNTHESIZER (AI-SE)")
    print("="*60 + "\033[0m")

    print("[*] Gathering context from Neo4j for Social Engineering...")
    
    # In a real run, you'd pull data about employees or internal tech found by other agents
    target_person = input("[?] Target Name/Email: ").strip()
    context = input("[?] Context (e.g., 'Internal Joomla migration', 'Docker outage'): ").strip()

    prompt = (
        f"You are a professional Red Team operator. Write a convincing internal email to {target_person} "
        f"referencing a {context}. The goal is to get them to click a link or check a config file. "
        "Make it look urgent but corporate. Do not include headers, just the body."
    )

    print(f"[*] Synthesizing persona for {target_person}...")

    try:
        response = requests.post('http://localhost:11434/api/generate', 
                                json={
                                    "model": "llama3",
                                    "prompt": prompt,
                                    "stream": False
                                })
        
        email_body = response.json().get('response', '')
        print("\033[92m" + "="*40 + "\n[+] SYNTHESIZED EMAIL:\n" + "="*40 + "\n" + email_body + "\n" + "="*40 + "\033[0m")

        db.report_finding("63_Intel_Synthesizer", "Phishing_Template_Generated", {
            "target": target_person,
            "context": context
        })
    except Exception as e:
        print(f"[-] LLM unreachable: {e}")

    db.close()

if __name__ == "__main__":
    run()
