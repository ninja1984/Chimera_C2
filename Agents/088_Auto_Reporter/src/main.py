import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
from datetime import datetime
import logging

# The GPS line for project navigation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Auto_Reporter:
    def __init__(self):
        self.agent_id = "81"
        self.name = "Auto_Reporter"
        self.db = ChimeraDB()
        self.report_dir = "/home/dan/Chimera_Project/loot/reports/"
        
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def generate_markdown(self):
        """Queries Neo4j and builds a structured Markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        report_file = f"{self.report_dir}CHIMERA_SUMMARY_{timestamp}.md"
        
        # Query for all findings
        query = "MATCH (f:Finding) RETURN f.agent as agent, f.type as type, f.data as data, f.severity as severity ORDER BY f.severity DESC"
        
        try:
            with self.db.driver.session() as session:
                results = list(session.run(query))
            
            with open(report_file, "w") as f:
                f.write(f"# 🛡️ CHIMERA SWARM EXECUTION REPORT\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## 📊 Executive Summary\n")
                f.write(f"Total Vulnerabilities Identified: **{len(results)}**\n\n")
                
                f.write(f"| Severity | Agent | Vulnerability Type | Details |\n")
                f.write(f"| :--- | :--- | :--- | :--- |\n")
                
                for r in results:
                    severity = r['severity'] if r['severity'] else "INFO"
                    # Add some emoji flair based on severity
                    sev_icon = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡"
                    
                    f.write(f"| {sev_icon} {severity} | {r['agent']} | {r['type']} | {r['data']} |\n")
                
                f.write(f"\n\n---\n*End of Chimera Automated Report - Agent 81 Out.*")

            return report_file
        except Exception as e:
            return f"Error generating report: {e}"

    def run(self):
        # Setup logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        path = self.generate_markdown()
        print(f"[+] Report generated successfully: {path}")
        self.db.close()

if __name__ == "__main__":
    agent = Auto_Reporter()
    agent.run()
