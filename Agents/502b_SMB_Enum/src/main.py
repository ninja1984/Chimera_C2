#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import struct
import sys

class SMBEnumEngine:
    """
    Agent 502.b: Raw SMB Dialect & OS Fingerprinter.
    Constructs raw NetBIOS/SMB1 packets to force the target kernel 
    to reveal its exact build version and memory architecture, 
    a strict prerequisite for memory-corruption exploitation.
    """
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.port = 445
        self.timeout = 5.0

    def craft_negotiate_request(self):
        """Actionable: Manually packing the SMB Header and Payload."""
        # 1. NetBIOS Session Service Header
        # Type: 0x00 (Session Message)
        # Length: 0x00000055 (85 bytes of SMB data to follow)
        netbios = struct.pack(">B I", 0x00, 0x00000055)[0:4]

        # 2. SMB Header
        # Protocol: \xFFSMB
        # Command: 0x72 (Negotiate Protocol)
        # Status/Flags/Flags2/PID/UID/MID/TID (Zeroed for initial request)
        smb_header = struct.pack(
            "<4s B I H H 8s H H H H H",
            b"\xffSMB", 0x72, 0x00000000, 0x18, 0x0128, 
            b"\x00"*8, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000
        )

        # 3. SMB Payload (Dialects we want to test)
        dialects = b"\x02NT LM 0.12\x00\x02SMB 2.002\x00\x02SMB 2.???\x00"
        word_count = struct.pack("<B", 0x00)
        byte_count = struct.pack("<H", len(dialects))
        
        payload = word_count + byte_count + dialects

        return netbios + smb_header + payload

    def execute(self):
        print(f"--- [AGENT 502.b: RAW SMB ENUMERATION] ---")
        print(f"[*] Target: {self.target_ip}:445")

        packet = self.craft_negotiate_request()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.target_ip, self.port))
            
            print("[*] Sending Raw Negotiate Protocol Request...")
            s.send(packet)
            
            response = s.recv(1024)
            s.close()

            if not response:
                print("[\033[91mFAILED\033[0m] No response from target.")
                return

            self._parse_response(response)

        except Exception as e:
            print(f"[\033[91mFAILED\033[0m] Connection error: {e}")

    def _parse_response(self, data):
        """Extracts the Native OS string from the SMB response."""
        if len(data) < 36:
            print("[!] Invalid SMB response length.")
            return

        # Check for \xFFSMB signature
        if data[4:8] != b"\xffSMB":
            print("[!] Not an SMB1 response. Target may require SMB2/3 negotiation.")
            return

        print("[\033[92mSUCCESS\033[0m] Valid SMB Response Received.")
        
        # The Native OS and LAN Manager strings are usually at the end of the payload
        # in a standard SMB1 Negotiate Response. We search for printable strings.
        try:
            # Skip NetBIOS and SMB Header (36 bytes)
            payload = data[36:]
            
            # Very basic string extraction for the POC
            strings = [s for s in payload.split(b'\x00') if len(s) > 2]
            
            print("\n[+] Extracted Target Metadata:")
            for s in strings:
                try:
                    decoded = s.decode('utf-16le') if b'\x00' in s else s.decode('ascii', errors='ignore')
                    if any(c.isalpha() for c in decoded):
                        print(f"    -> {decoded.strip()}")
                except: pass
                
            print("\n[*] Ready for architecture-specific offset mapping.")
        except Exception as e:
            print(f"[!] Parsing error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip>")
        sys.exit(1)
    
    SMBEnumEngine(sys.argv[1]).execute()
