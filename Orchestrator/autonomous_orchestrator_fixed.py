#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/dan/Chimera_C2')
from chimera_config import get_c2_host, get_c2_port, get_gpu_ip

GPU_IP = get_gpu_ip()
C2_HOST = get_c2_host()
C2_PORT = get_c2_port()

print(f"[*] Connecting to C2 at {C2_HOST}:{C2_PORT}")
print(f"[*] GPU at {GPU_IP}")
