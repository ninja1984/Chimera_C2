#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess
import sys

class SwarmConsensus:
    """
    Agent 506: Autonomous Leader Election.
    Compiles and runs the C-native state machine to determine 
    which node will act as the external bridge for the Swarm.
    """
    def execute(self):
        src = "/home/dan/Chimera_Project/agents/506_Swarm_Consensus/src/election.c"
        bin_out = "/home/dan/Chimera_Project/agents/506_Swarm_Consensus/src/election"
        
        # Compile the consensus engine
        subprocess.run(["gcc", src, "-o", bin_out], check=True)
        
        # Run the election protocol
        try:
            subprocess.run([bin_out])
        except KeyboardInterrupt:
            print("\n[*] Election protocol terminated.")

if __name__ == "__main__":
    SwarmConsensus().execute()
