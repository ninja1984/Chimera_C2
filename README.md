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
---

## ⚔️ The Arsenal: Tactical Modules

While the Orchestrator handles the high-level strategy and graph mapping, the actual execution is distributed across specialized agent modules.

### 1. The Vanguard (`spear.py` / `liveexploit`)
The Vanguard acts as the directed strike module. When the Orchestrator identifies a vulnerable node in the topology, `spear.py` is tasked with the direct engagement.
* **Usage:** `python3 spear.py --target <IP_ADDRESS>`
* **Role:** Precision execution, targeted enumeration, and localized payload delivery.

### 2. The Hive (`hive.py` / `live_hive.py`)
The swarm intelligence logic. Instead of relying on a single top-down command queue, the Hive distributes situational awareness and operational tasks across multiple active agents.
* **Usage:** `python3 hive.py`
* **Role:** Autonomous lateral movement simulation, multi-agent task distribution, and redundant command execution.

### 3. Leviathan Catcher (`leviathan_catcher.py`)
The persistent backend listener. Once a node is compromised by the Vanguard or the Hive, it establishes a callback to the Leviathan Catcher to maintain state and session persistence without dropping the primary LLM context.
* **Usage:** `python3 leviathan_catcher.py` (typically run in a detached screen/tmux session on the C2 server)
* **Role:** Asynchronous session management, reverse-connection handling, and heartbeat monitoring for compromised nodes.

