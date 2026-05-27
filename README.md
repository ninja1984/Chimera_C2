# Chimera C2: Autonomous Multi-Agent Red Team Framework

Chimera C2 is a comprehensive Python-based, Multi-Agent orchestration framework. It leverages local LLMs (via Ollama) to autonomously map networks, reason about attack vectors, and deploy specialized agent modules within a simulated target environment.

## 🧠 Core Architecture & The Hive
Chimera is broken down into a command-and-control brain and specialized tactical agents:

* **Autonomous Orchestrator (`autonomous_orchestrator.py`):** The main Llama-driven Coordinator. Analyzes live topology graphs, issues commands, and halts for Human-in-the-Loop (HITL) overrides.
* **The Backend Sandbox (`live_orchestrator_backend.py`):** The simulated target environment and validation engine that tracks node states (BLIND, DISCOVERED, COMPROMISED) and enforces routing limits.
* **The Vanguard / Spear (`spear.py` / `liveexploit`):** Tactical execution scripts designed for directed operations against specific targets identified by the Orchestrator.
* **The Hive (`hive.py` / `live_hive.py`):** The multi-agent swarm logic handling distributed tasks and inter-agent communication.
* **Leviathan Catcher (`leviathan_catcher.py`):** Handles reverse connections and persistent callbacks from compromised nodes.
* **Infrastructure (`c2_server.py` / `ignite_brain.sh`):** Core networking utilities and startup scripts for standing up the C2 infrastructure.

## 🚀 How to Run the Environment

### 1. Start the Target Simulation
Boot up the virtual target range in the background:
`python3 live_orchestrator_backend.py`

### 2. Ignite the Brain (LLM Routing)
Ensure your local machine is port-forwarded to your remote GPU running Ollama. Use the startup script or run:
`ssh -N -L 11434:127.0.0.1:11434 root@<VAST_AI_IP>`

### 3. Launch the Orchestrator
Start the HITL UI and AI execution loop:
`GPU_IP="127.0.0.1" python3 autonomous_orchestrator.py`

### 4. Deploy the Swarm
Once initial footholds are established by the Orchestrator, launch the Hive and Leviathan components to maintain persistence and expand the attack surface.
