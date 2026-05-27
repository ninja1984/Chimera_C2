import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
from ldap3 import Server, Connection, ALL, SUBTREE # pip install ldap3

# The GPS line for project navigation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class AD_Analyzer:
    def __init__(self):
        self.agent_id = "74"
        self.name = "AD_Analyzer"
        self.db = ChimeraDB()
        
        # In a real scenario, these would be harvested by Agent 52 (Credential Harvester)
        self.domain = "CHIMERA.LOCAL"
        self.dc_ip = "10.10.10.100" 
        self.user = "CHIMERA\\Guest"
        self.password = "Password123!"

    def enumerate_domain(self):
        """Connects to LDAP and maps out the Domain Admins."""
        server = Server(self.dc_ip, get_info=ALL)
        try:
            conn = Connection(server, user=self.user, password=self.password, auto_bind=True)
            self.logger.info(f"[+] Successfully bound to Domain Controller: {self.dc_ip}")

            # Search for Domain Admins
            search_filter = "(&(objectCategory=person)(objectClass=user)(adminCount=1))"
            conn.search(search_base="DC=CHIMERA,DC=LOCAL",
                        search_filter=search_filter,
                        attributes=['sAMAccountName', 'description'])

            admins = []
            for entry in conn.entries:
                admins.append(entry.sAMAccountName.value)
                self.db.report_finding(self.name, "AD_Admin_Found", {
                    "username": entry.sAMAccountName.value,
                    "description": str(entry.description)
                })

            self.logger.warning(f"[!] Found {len(admins)} potential Domain Admins.")
            conn.unbind()
            return admins
        except Exception as e:
            self.logger.error(f"LDAP Connection failed: {e}")
            return []

    def run(self):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        self.enumerate_domain()
        self.db.close()

if __name__ == "__main__":
    agent = AD_Analyzer()
    agent.run()
