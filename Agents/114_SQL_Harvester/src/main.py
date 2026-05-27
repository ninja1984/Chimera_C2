import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
import bloodhound
from bloodhound.ad.domain import AD
from bloodhound.ad.authentication import ADAuthentication

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Active_Directory_Scout:
    def __init__(self):
        self.agent_id = "06"
        self.name = "Active_Directory_Scout"
        self.base_dir = "/home/dan/Chimera_Project/agents/Active_Directory_Scout"
        
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

    def run_bloodhound_scan(self, domain, username, password, dc_ip):
        """
        Uses the BloodHound.py logic to ingest AD data.
        Note: This usually generates JSON files which we then ingest into Neo4j.
        """
        self.logger.info(f"Initiating AD Scout for domain: {domain}")
        self.db.heartbeat(self.name)

        try:
            # Initialize the AD object
            ad = AD(domain=domain, dns_server=dc_ip)
            
            # Setup Authentication
            auth = ADAuthentication(username=username, password=password, domain=domain)
            
            # Initialize BloodHound Collector
            # Collection methods: Group, LocalAdmin, Session, Trusts, ACL, etc.
            bg = bloodhound.BloodHound(ad)
            bg.auth = auth
            
            self.logger.info("[*] Starting data collection (this may take a minute)...")
            
            # This will collect and write JSON files to the current directory
            bg.run(collect=['Group', 'LocalAdmin', 'Session', 'Trusts', 'ACL', 'ObjectProps'],
                   num_workers=4)
            
            self.logger.info("[+] AD Ingestion complete. JSON files generated.")
            
            # Logic to report the successful scan back to the graph
            finding_data = {
                "domain": domain,
                "domain_controller": dc_ip,
                "status": "Enumeration Complete",
                "collector": "BloodHound.py"
            }
            self.db.report_finding(self.name, "AD_Domain", finding_data)

        except Exception as e:
            self.logger.error(f"AD Scouting failed: {e}")

    def run(self):
        self.logger.info(f"{self.name} checking for target domain credentials...")
        
        # Placeholder for targets found in previous stages
        # In a real run, this would be triggered by 'Credential_Stasher' or 'Network_Mapper'
        target_domain = "CORP.LOCAL"
        target_user = "dan.svc" 
        target_pass = "Dan7001524" # Using your set password as a test
        target_dc = "10.129.6.1"
        
        # Uncomment below to run when you have a live target
        # self.run_bloodhound_scan(target_domain, target_user, target_pass, target_dc)
        
        self.db.close()

if __name__ == "__main__":
    agent = Active_Directory_Scout()
    agent.run()
