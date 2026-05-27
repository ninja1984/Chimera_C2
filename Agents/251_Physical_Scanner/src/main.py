#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class PhysicalScanner:
    """
    Agent 315: Hardware Interface & DMA Auditor.
    Identifies physical hardware vulnerabilities (Thunderbolt/PCIe) 
    that allow for out-of-band memory extraction.
    """
    def check_dma_interfaces(self):
        print("[*] Auditing PCI/Thunderbolt DMA vulnerability status...")
        try:
            # Check for Thunderbolt controllers
            lspci = subprocess.check_output(["lspci"]).decode().lower()
            if "thunderbolt" in lspci:
                print("[!!!] WARNING: Thunderbolt controller detected. Potential DMA Vector.")
            
            # Check for IOMMU (The hardware defense against DMA attacks)
            dmesg = subprocess.check_output(["dmesg"]).decode().lower()
            if "iommu" in dmesg and ("enabled" in dmesg or "on" in dmesg):
                return "SECURE (IOMMU Active)"
            else:
                return "VULNERABLE (No IOMMU protection found)"
        except: return "Unknown"

    def execute(self):
        print("--- [AGENT 315: PHYSICAL INTERFACE AUDIT] ---")
        status = self.check_dma_interfaces()
        print(f"[+] DMA Security Status: {status}")

if __name__ == "__main__":
    PhysicalScanner().execute()
