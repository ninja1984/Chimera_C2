# Chimera C2: Autonomous Multi-Agent Red Team Framework

Chimera C2 is an advanced, autonomous Red Team orchestration framework. It utilizes local Large Language Models (LLMs) to perform complex network reconnaissance, adaptive lateral movement, and modular tactical exploitation.

## 📁 Repository Structure
The framework is partitioned into functional modules to separate strategy from tactical execution:

- `Orchestrator/`: The central intelligence hub. Contains the Llama-driven logic that processes network topology, reasons about attack vectors, and manages the Human-in-the-Loop (HITL) command interface.
- `Agents/`: An extensive library of 300+ specialized tactical agents. Each subdirectory (e.g., `188_Shadow_DB`, `177_TTY_Hijacker`) contains a self-contained module designed for specific mission objectives.
- `Vanguard/`: Tactical strike modules, including the `spear.py` directed engagement tool and `leviathan_catcher.py` for persistent reverse-connection management.
- `Infrastructure/`: Core network utilities, proxy configurations, and initialization scripts (`ignite_brain.sh`) required to stand up the C2 environment.
- `Tier2_C_Agents/`: High-performance C/C++ agent cores (`agent_186v_core.c`, `chimera_ghost.c`) for low-level system interaction and kernel-space operations.

## 🚀 Operational Workflow

### 1. Initialization
Stand up the target simulation environment:
```bash
python3 Orchestrator/live_orchestrator_backend.py


2. Brain Activation

Ensure your local LLM (Ollama) is running and accessible. Use the startup script to link the orchestrator:
Bash

GPU_IP="127.0.0.1" python3 Orchestrator/autonomous_orchestrator.py

3. Tactical Deployment

Once the Orchestrator identifies a target node, you can trigger tactical modules from the Vanguard or Agents library:

    Directed Strike: Use spear.py to engage specific nodes.

    Persistence: Use leviathan_catcher.py in a detached session to maintain callbacks.

    Swarm Operations: Use hive.py to distribute intelligence across identified nodes.

🔐 Security & Compliance

This framework is strictly for authorized security auditing and educational purposes. Ensure all network simulations are performed within isolated environments. Never include local credentials, private tokens, or sensitive loot in tracked files. Use the .gitignore file provided to mask sensitive local data.


## Configuration
All IPs use environment variables.

Setup:
  cp config/.env.example config/.env
  source config/.env

Variables: C2_HOST, C2_PORT, CALLBACK_HOST, CALLBACK_PORT, GPU_IP

## Configuration Setup

1. Copy environment template:
   cp config/.env.example config/.env

2. Edit with your lab values:
   nano config/.env

3. Source before running:
   source config/.env
   python3 Orchestrator/autonomous_orchestrator.py

All hardcoded IPs removed - uses environment variables only.
