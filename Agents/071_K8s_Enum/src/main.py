import os
import sys
import subprocess

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[36m" + "="*60)
    print("   CHIMERA AGENT 64 :: K8s_ENUM (CLUSTER ENUMERATOR)")
    print("="*60 + "\033[0m")

    token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    
    print("[*] Checking for Kubernetes Service Account Token...")

    if os.path.exists(token_path):
        print("\033[92m[+] SUCCESS: K8s Token Found!\033[0m")
        
        try:
            # 1. Check permissions (Can we list pods?)
            cmd = "kubectl get pods"
            output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode()
            print(f"[*] Cluster Access Level:\n{output}")
            
            db.report_finding("64_K8s_Enum", "K8s_Token_Discovered", {
                "token_location": token_path,
                "can_list_pods": True,
                "severity": "HIGH"
            })
        except Exception:
            print("[-] Token found but 'kubectl' not installed or permissions restricted.")
    else:
        print("[-] Not running inside a standard K8s pod environment.")

    db.close()

if __name__ == "__main__":
    run()
