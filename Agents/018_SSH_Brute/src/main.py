import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import logging

class Agent_13:
    def __init__(self):
        self.agent_id = "13"
        self.name = "Agent_13"
        self.base_path = "/home/dan/Chimera_Project/agents/{self.name}"
        
        # Setup specific logging
        logging.basicConfig(
            filename=f"/home/dan/Chimera_Project/logs/{self.name}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)

    def run(self):
        self.logger.info(f"{self.name} is online and operational on M2 drive.")
        print(f"[*] {self.name} reporting for duty.")


    def pulse(self):
        try:
            from core.db_handler import ChimeraDB
            db = ChimeraDB()
            db.heartbeat(self.name)
            self.logger.info("Heartbeat sent to Neo4j.")
            db.close()
        except Exception as e:
            self.logger.error(f"Heartbeat failed: {e}")

if __name__ == "__main__":
    agent = Agent_13()
    agent.run()
