import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import subprocess
import logging
import signal

# Ensure the agent can find the core directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Proxy_Relay:
    def __init__(self):
        self.agent_id = "09"
        self.name = "Proxy_Relay"
        self.base_dir = "/home/dan/Chimera_Project/agents/Proxy_Relay"
        
        # Setup Logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(logging.StreamHandler())
        
        self.db = ChimeraDB()
        self.process = None

    def start_chisel_server(self, port=8080):
        """
        Starts a Chisel server on Kali to accept reverse tunnels from compromised hosts.
        """
        self.logger.info(f"Starting Chisel Server on port {port}...")
        self.db.heartbeat(self.name)

        cmd = ["chisel", "server", "--port", str(port), "--reverse"]
        
        try:
            # Run the server in the background
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.logger.info(f"[+] Chisel Server is UP. PID: {self.process.pid}")
            
            finding_data = {
                "proxy_type": "Chisel Reverse",
                "port": port,
                "status": "Listening",
                "description": "Awaiting reverse connection from pivot host"
            }
            self.db.report_finding(self.name, "Infrastructure", finding_data)

        except Exception as e:
            self.logger.error(f"Failed to start Chisel server: {e}")

    def stop_relay(self):
        """Kills the active proxy process."""
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.logger.info("Proxy_Relay process terminated.")

    def run(self):
        self.logger.info(f"{self.name} sequence initiated.")
        # Default behavior: Start the relay server to wait for a victim to connect back
        self.start_chisel_server()
        
        # In a real swarm, this would stay running to maintain the tunnel
        # For now, we keep the object alive.
        # self.db.close() 

if __name__ == "__main__":
    agent = Proxy_Relay()
    try:
        agent.run()
        # Keep the script running to maintain the tunnel until Ctrl+C
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        agent.stop_relay()
