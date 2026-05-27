import os
import sys
from datetime import datetime

def run_master_audit(target_ip):
    """
    Synthesizes findings from all 199 agents into a single actionable report.
    """
    print(f"[*] [Agent 200] The Auditor: Synthesizing Chimera Report for {target_ip}...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agents_root = os.path.dirname(script_dir) # Moves up to /agents/
    project_root = os.path.dirname(agents_root) # Moves up to /Chimera_Project/
    
    report_path = os.path.join(script_dir, "..", "loot", f"FINAL_REPORT_{target_ip}.md")
    
    report_content = [
        f"# PROJECT CHIMERA: STRATEGIC AUDIT REPORT",
        f"**Target:** {target_ip}",
        f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n---",
        "## EXECUTIVE SUMMARY",
        "The following vulnerabilities were identified across the 200-agent swarm deployment.",
        "\n---",
        "## TECHNICAL FINDINGS BY VECTOR"
    ]

    # Walk through every agent folder to find 'loot' files
    found_data = False
    for agent_folder in sorted(os.listdir(agents_root)):
        agent_path = os.path.join(agents_root, agent_folder)
        loot_dir = os.path.join(agent_path, "loot")
        
        if os.path.isdir(loot_dir):
            for loot_file in os.listdir(loot_dir):
                file_path = os.path.join(loot_dir, loot_file)
                if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                    found_data = True
                    report_content.append(f"\n### SOURCE: {agent_folder} ({loot_file})")
                    with open(file_path, "r") as f:
                        lines = f.readlines()[-10:] # Grab last 10 findings for the summary
                        for line in lines:
                            report_content.append(f"- {line.strip()}")

    if not found_data:
        report_content.append("\n[!] No critical findings identified by the swarm.")

    # Write the Final Markdown Report
    with open(report_path, "w") as f:
        f.write("\n".join(report_content))
    
    print(f"[SUCCESS] Master Audit Report generated: {report_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_ip>")
        sys.exit(1)
    
    run_master_audit(sys.argv[1])
