import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests
import logging

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Web_Fuzzer_Pro:
    def __init__(self):
        self.agent_id = "35"
        self.name = "Web_Fuzzer_Pro"
        self.db = ChimeraDB()
        
        # Setup Logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())

        # Small built-in wordlist for quick wins
        self.wordlist = ["admin", "login", "config", "backup", "api", "dev", "shell", "phpmyadmin", ".env", ".git"]

    def fuzz(self, target_ip, port=80):
        """Iterates through wordlist to find hidden directories."""
        self.logger.info(f"Fuzzing http://{target_ip}:{port} for hidden directories...")
        
        for word in self.wordlist:
            url = f"http://{target_ip}:{port}/{word}"
            try:
                # We use allow_redirects=False to catch 301/302 specifically
                response = requests.get(url, timeout=3, allow_redirects=False)
                
                if response.status_code in [200, 301, 302, 403]:
                    self.logger.warning(f"[!] INTERESTING PATH FOUND: {url} ({response.status_code})")
                    self.db.report_finding(self.name, "Web_Path_Discovery", {
                        "url": url,
                        "status": response.status_code,
                        "ip": target_ip
                    })
            except requests.exceptions.RequestException:
                continue

    def run(self):
        self.db.heartbeat(self.name)
        # Query Neo4j for any hosts that have web ports open
        query = "MATCH (h:Host)-[:HAS_PORT]->(p:Port) WHERE p.port IN [80, 8080, 443] RETURN h.ip as ip, p.port as port"
        with self.db.driver.session() as session:
            result = session.run(query)
            for record in result:
                self.fuzz(record["ip"], record["port"])
        self.db.close()

if __name__ == "__main__":
    agent = Web_Fuzzer_Pro()
    agent.run()
