import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import asyncio
import logging
from bleak import BleakScanner # pip install bleak

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Bluetooth_Leaker:
    def __init__(self):
        self.agent_id = "75"
        self.name = "Bluetooth_Leaker"
        self.db = ChimeraDB()
        self.found_devices = []

    async def scan(self):
        """Asynchronous scan for BLE devices."""
        self.logger.info("Initiating modern BLE proximity scan (10s)...")
        try:
            devices = await BleakScanner.discover(timeout=10.0)
            for d in devices:
                # d.address is the MAC, d.name is the SSID-like name
                name = d.name if d.name else "Unknown_Device"
                rssi = d.rssi # Signal strength (helps calculate distance)
                
                self.logger.warning(f"[!] BLE Device: {name} | MAC: {d.address} | RSSI: {rssi}")
                
                self.db.report_finding(self.name, "BLE_Device_Proximate", {
                    "mac": d.address,
                    "name": name,
                    "signal_strength": rssi
                })
        except Exception as e:
            self.logger.error(f"BLE Scan failed: {e}. Check if bluetooth is enabled.")

    def run(self):
        # Setup logging
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(self.name)
        
        self.db.heartbeat(self.name)
        
        # We have to run the async scan in a loop
        asyncio.run(self.scan())
        
        self.db.close()

if __name__ == "__main__":
    # REQUIRED: pip install bleak
    agent = Bluetooth_Leaker()
    agent.run()
