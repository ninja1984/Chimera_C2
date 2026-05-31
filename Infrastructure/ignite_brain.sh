#!/bin/bash

# --- VAST.AI CLOUD CONFIGURATION ---
REMOTE_PORT="50923"
REMOTE_USER="root"
REMOTE_IP="70.55.99.180"
# -----------------------------------

echo -e "\033[1;34m[*] Initiating Project Chimera Phase 4: Nation-State Uplink (LIVE FIRE)\033[0m"

pkill -f "ssh.*-L 11434:localhost:11434" 2>/dev/null

echo "[*] Opening encrypted SSH Wormhole to A6000 ($REMOTE_IP:$REMOTE_PORT)..."
ssh -p $REMOTE_PORT $REMOTE_USER@$REMOTE_IP -N -f -L 11434:localhost:11434 -o StrictHostKeyChecking=no

sleep 3

echo "[*] Wormhole established. Waking WhiteRabbitNeo..."
echo "=================================================="
python3 autonomous_handler_loop.py
echo "=================================================="

pkill -f "ssh.*-L 11434:localhost:11434" 2>/dev/null
echo -e "\033[1;32m[+] Connection severed. OPSEC secured.\033[0m"
