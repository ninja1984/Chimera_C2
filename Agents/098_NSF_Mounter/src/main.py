import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class NFS_Mounter:
    def __init__(self):
        self.agent_id = "21"
        self.name = "NFS_Mounter"
        self.base_dir = "/home/dan/Chimera_Project/agents/NFS_Mounter"
        self.mount_base = "/tmp/chimera_mounts"
        
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
        
        if not os.path.exists(self.mount_base):
            os.makedirs(self.mount_base)

    def check_nfs_shares(self, target_ip):
        """
        Uses 'showmount' to list exported shares on the target.
        """
        self.logger.info(f"Checking NFS exports on {target_ip}...")
        self.db.heartbeat(self.name)

        try:
            # -e lists exports
            result = subprocess.run(["showmount", "-e", target_ip], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                shares = result.stdout.strip()
                self.logger.info(f"[!] Found NFS Shares on {target_ip}:\n{shares}")
                
                finding_data = {
                    "ip": target_ip,
                    "shares": shares,
                    "vulnerability": "NFS Export Exposed"
                }
                self.db.report_finding(self.name, "NetworkShare", finding_data)
                
                # Check for the holy grail: no_root_squash usually allows world-writable/root-accessible shares
                if "*" in shares or "everyone" in shares.lower():
                    self.logger.warning(f"[!!!] Potential insecure NFS configuration on {target_ip}")
                
                return True
        except Exception as e:
            self.logger.error(f"NFS check failed on {target_ip}: {e}")
        return False

    def get_nfs_targets(self):
        """
        Queries Neo4j for Hosts with Port 2049 open.
        """
        query = "MATCH (h:Host)-[:HAS_PORT]->(p:Port {port: 2049}) RETURN h.ip AS ip"
        targets = []
        with self.db.driver.session() as session:
            result = session.run(query)
            for record in result:
                targets.append(record["ip"])
        return targets

    def run(self):
        self.logger.info(f"{self.name} searching graph for NFS targets...")
        targets = self.get_nfs_targets()
        
        if not targets:
            self.logger.info("No NFS targets (Port 2049) found in graph.")
            return

        for ip in targets:
            self.check_nfs_shares(ip)
            
        self.db.close()

if __name__ == "__main__":
    agent = NFS_Mounter()
    agent.run()
