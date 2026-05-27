import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import re
import logging

# The GPS line we just discussed!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Static_Fuzzer:
    def __init__(self):
        self.agent_id = "56"
        self.name = "Static_Fuzzer"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def analyze_file(self, file_path):
        """Scans a file for 'Sinks' (dangerous functions)."""
        # We use Regex (Regular Expressions) to find dangerous patterns
        sinks = [
            r"system\(", r"eval\(", r"exec\(", r"subprocess\.run\(", 
            r"shell=True", r"pickle\.load\("
        ]
        
        findings = []
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    for sink in sinks:
                        if re.search(sink, line):
                            finding = f"Line {i+1}: Potential Sink found -> {line.strip()}"
                            self.logger.warning(f"[!] {finding}")
                            findings.append(finding)
            
            if findings:
                # Report to the Brain
                self.db.report_finding(self.name, "Code_Vulnerability", {
                    "file": file_path,
                    "findings": findings,
                    "severity": "HIGH"
                })
        except Exception as e:
            self.logger.error(f"Analysis failed for {file_path}: {e}")

    def run(self):
        self.db.heartbeat(self.name)
        # This agent would be pointed at a directory of harvested code
        # self.analyze_file("/tmp/downloaded_app/app.py")
        self.db.close()

if __name__ == "__main__":
    agent = Static_Fuzzer()
    agent.run()
