import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import time
import logging
from scapy.all import * # pip install scapy

# The GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Network_Advertiser:
    def __init__(self):
        self.agent_id = "64"
        self.name = "Network_Advertiser"
        self.db = ChimeraDB()
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def poison_callback(self, packet):
        """Listens for LLMNR/NBNS queries and logs them."""
        # LLMNR uses UDP Port 5355
        if packet.haslayer(UDP) and packet[UDP].dport == 5355:
            query_name = packet[Raw].load.decode('utf-8', 'ignore')
            self.logger.warning(f"[!] Captured LLMNR Query for: {query_name}")
            
            # In a full attack, we'd use Responder, but for this PoC, 
            # we log the potential victim IP to the Brain.
            self.db.report_finding(self.name, "LLMNR_Query_Intercepted", {
                "victim_ip": packet[IP].src,
                "requested_resource": query_name
            })

    def run(self):
        self.db.heartbeat(self.name)
        self.logger.info("Starting LLMNR listener (Passive Mode)...")
        
        # Sniffing requires root/sudo
        try:
            sniff(filter="udp port 5355", prn=self.poison_callback, store=0)
        except Exception as e:
            self.logger.error(f"Sniffer failed: {e}. Are you running as sudo?")

if __name__ == "__main__":
    agent = Network_Advertiser()
    agent.run()
