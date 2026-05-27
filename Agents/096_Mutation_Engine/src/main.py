import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import requests
import json
import logging

# Ensure the agent can find the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Mutation_Engine:
    def __init__(self):
        self.agent_id = "51"
        self.name = "Mutation_Engine"
        self.db = ChimeraDB()
        self.ollama_url = "http://localhost:11434/api/generate"
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def ask_llm_to_fix(self, original_code, error_message):
        """Sends broken code to Ollama and gets a fixed version."""
        prompt = f"""
        You are an expert Cybersecurity Python Coder. 
        The following script failed with an error. 
        Rewrite the ENTIRE script to fix the error and make it more stealthy.
        Return ONLY the raw python code. No explanations.

        ERROR: {error_message}
        
        CODE:
        {original_code}
        """
        
        payload = {
            "model": "codellama", # Or "llama3" depending on what you have pulled
            "prompt": prompt,
            "stream": False
        }

        try:
            self.logger.info("Requesting code mutation from Ollama...")
            response = requests.post(self.ollama_url, json=payload)
            fixed_code = response.json().get('response', '')
            return fixed_code
        except Exception as e:
            self.logger.error(f"LLM Connection failed: {e}")
            return None

    def mutate_agent(self, agent_path, error_log):
        """Reads a failing agent, gets a fix, and updates the file."""
        if os.path.exists(agent_path):
            with open(agent_path, 'r') as f:
                old_code = f.read()
            
            new_code = self.ask_llm_to_fix(old_code, error_log)
            
            if new_code:
                with open(agent_path, 'w') as f:
                    f.write(new_code)
                self.logger.warning(f"[+++] MUTATION COMPLETE: {agent_path} has been evolved.")
                self.db.report_finding(self.name, "Code_Mutation", {
                    "agent": agent_path,
                    "status": "Evolved"
                })

    def run(self):
        self.db.heartbeat(self.name)
        # This would be triggered by the Orchestrator when a log contains 'Error'
        # self.mutate_agent("agents/Network_Mapper/src/main.py", "SyntaxError: invalid syntax")
        self.db.close()

if __name__ == "__main__":
    engine = Mutation_Engine()
    engine.run()
