import subprocess
import os
from neo4j import GraphDatabase

# ==============================================================================
# PROJECT CHIMERA: AUTOMATED SWEEP SCOUT
# Purpose: Scan subnet and autonomously populate the Tactical Map (Neo4j).
# ==============================================================================

class SweepScout:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = "Dan7001524"
        self.subnet = "10.0.2." # Lab Subnet

    def push_to_graph(self, ip):
        """Autonomously injects discovered hosts into the Brain's sight."""
        try:
            driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            with driver.session() as session:
                # MERGE ensures we don't create duplicates, only update if new
                session.run("""
                    MERGE (h:Host {ip: $ip})
                    ON CREATE SET h.status = 'DISCOVERED', h.os = 'Unknown', h.last_seen = timestamp()
                """, ip=ip)
            driver.close()
            return True
        except Exception as e:
            print(f"[-] Scout Graph Error: {e}")
            return False

    def run_sweep(self):
        print(f"[*] Scout: Scanning {self.subnet}0/24...")
        # Using fping if available for speed, fallback to standard ping
        for i in range(1, 254):
            ip = f"{self.subnet}{i}"
            # Quick ping check (1 second timeout)
            res = subprocess.call(['ping', '-c', '1', '-W', '1', ip], 
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res == 0:
                print(f"[+] Scout: Host Active -> {ip}")
                self.push_to_graph(ip)

if __name__ == "__main__":
    scout = SweepScout()
    scout.run_sweep()
