import os
import sys
from datetime import datetime

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[92m" + "="*60)
    print("   CHIMERA AGENT 59 :: FINAL REPORT GENERATOR")
    print("="*60 + "\033[0m")

    report_date = datetime.now().strftime("%Y-%m-%d")
    report_file = f"/home/dan/Chimera_Project/loot/CHIMERA_REPORT_{report_date}.md"

    print(f"[*] Compiling findings from Neo4j...")

    # Logic: Pull all nodes with severity 'CRITICAL' or 'HIGH'
    findings = db.get_all_findings() 

    with open(report_file, "w") as f:
        f.write(f"# PROJECT CHIMERA :: ENGAGEMENT REPORT\n")
        f.write(f"**Date:** {report_date}\n\n")
        f.write(f"## 1. Executive Summary\n")
        f.write(f"Automated swarm analysis has completed. Below is the attack chain and discovered vulnerabilities.\n\n")
        
        f.write(f"## 2. Critical Findings\n")
        for finding in findings:
            if finding.get('severity') == 'CRITICAL':
                f.write(f"### [!] {finding['type']}\n")
                f.write(f"- **Target:** {finding.get('target', 'N/A')}\n")
                f.write(f"- **Description:** {finding.get('description', 'No details provided.')}\n\n")

    print(f"\033[92m[+] Report generated successfully: {report_file}\033[0m")
    db.close()

if __name__ == "__main__":
    run()
