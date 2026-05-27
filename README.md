# Chimera C2: Autonomous Multi-Agent Red Team Framework

Chimera C2 is a Python-based, Multi-Agent orchestration framework designed to simulate autonomous network penetration testing. It leverages local LLMs (via Ollama) to parse simulated network states, reason about attack vectors, and execute targeted commands within a simulated sandbox environment.

## 🧠 Core Architecture
* **The Coordinator Agent (`llama3`):** Analyzes network topology, decides on the next operational action (e.g., discovery, enumeration, exploitation), and outputs strict JSON commands.
* **Human-in-the-Loop (HITL) Execution:** The framework halts before executing any AI-generated command, allowing a human operator to approve, deny, or inject contextual overrides directly into the AI's prompt history to correct hallucination loops.
* **Live Topology Graph:** A `rich`-powered dynamic terminal UI that updates target states (BLIND -> DISCOVERED -> COMPROMISED) in real-time based on backend simulation feedback.
* **Stateful Backend Simulation:** A separate validation engine that acts as the "target range," returning realistic JSON network maps and enforcing simulated firewall routing rules.

## 🛠️ Tech Stack
* **AI Backend:** Ollama (Llama 3 / CodeLlama) over SSH-tunneled REST API.
* **Frontend UI:** Textual/Rich for Python.
* **Networking:** Standard TCP Socket communication for backend target simulation.

## 🚀 Usage
1. Start the simulation backend: `python3 live_orchestrator_backend.py`
2. Start the AI Coordinator: `GPU_IP="127.0.0.1" python3 autonomous_orchestrator.py`
3. Supervise the AI via the interactive console prompts.
