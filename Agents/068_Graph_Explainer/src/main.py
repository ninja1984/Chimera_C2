import os
import sys

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[95m" + "="*60)
    print("   CHIMERA AGENT 61 :: GRAPH EXPLAINER (CYPHER TRANSLATOR)")
    print("="*60 + "\033[0m")

    print("[*] Analyzing shortest path to 'Domain Admin'...")

    # Logic: Cypher query to find the path from a known compromised user to a Root node
    # MATCH (start:User {compromised: true}), (end:User {name: 'root'}), 
    # path = shortestPath((start)-[*..10]->(end)) RETURN path
    
    path_data = db.find_attack_path("root")

    if path_data:
        print("\033[92m[+] ATTACK PATH DISCOVERED:\033[0m")
        # In a real run, this would loop through the nodes and explain the hops
        print("    [Start] -> Compromised Web User")
        print("    [Hop 1] -> Agent 57: Docker Socket Writable")
        print("    [Hop 2] -> Container Escape to Host")
        print("    [Target] -> Root Access achieved.")
    else:
        print("[-] No direct path to Root found yet. Keep rolling the swarm.")

    db.close()

if __name__ == "__main__":
    run()
