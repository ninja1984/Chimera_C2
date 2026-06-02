Chimera_C2 Framework

A from-scratch C2 framework built to understand offensive security tooling internals. No copy-paste - every component written manually to learn how these systems actually work.
Why I Built This

Transitioning from IT support to offensive security, I wanted to understand these tools from the inside out. Instead of running other people's exploits, I set out to rebuild core C2 functionality myself - learning how command & control systems manage agents, obfuscate traffic, and maintain persistence.

Core learning goal: Build working implementations of C2 concepts with zero reliance on copy-pasted code or obvious signatures. If I can't explain every line, it doesn't go in.
What's Actually Here

This is a research project developed over 3 months of focused work. The framework currently implements:

98 Specialized Offensive Agents (rapidly expanding)

Built from scratch with modular design. Each agent focuses on a specific red team task — from kernel diagnostics to advanced exfiltration.

    Tiered architecture - Separation between control logic and agent execution
    Modular components - Swappable communication methods and task handlers
    SQLite backend - Simple data persistence for testing/development

The "AI integration" mentioned in earlier versions refers to experimental LLM-assisted script generation and analysis tools - not autonomous decision-making agents. Think Copilot-style assistance, not autonomous orchestration.
Project Structure

Chimera_C2/
├── Agents/              # 98 agent implementations
├── Tier2_C_Agents/      # Secondary agent tier
├── Database/            # SQLite schemas and handlers
├── Modules/             # Task modules and communication handlers
└── config/               # Environment configuration

Current State

This is active development work, not a polished product. The ~15 commits you see represent iterative rebuilding as I learned - many experiments got scrapped when I understood better approaches. What's committed works; what doesn't was deleted, not hidden.
Technical Details

    Language: Python 3.x
    Database: SQLite (development), PostgreSQL planned
    Communication: HTTP/HTTPS with basic obfuscation
    Target platforms: Linux primarily, Windows agents in progress

What I Learned

    How C2 frameworks manage agent registration and tasking
    Practical obfuscation techniques that actually evade basic detection
    Why most "AI-powered" security tools are just regex with marketing
    The gap between "works in the lab" and "works in production"

Next Steps

    Staged payload delivery system
    Proper encryption for C2 traffic
    Windows agent hardening
    Detection evasion testing against real EDR
## Quick Start — How to Run Chimera C2

### Recommended LLM Setup (Important)
Chimera C2 was built and tested with **Ollama** using the following models:
- `whiterabbitneo`
- `obliteratus`

These models give the best reasoning and red-team behavior for the multi-agent system.

Make sure Ollama is running with one of these models before starting the orchestrator.


### 1. Environment Setup

```bash
cd /path/to/Chimera_C2

# 1. Create and edit the environment variables
cp config/.env.example config/.env     # if the example file exists
# OR create it manually:
cat > config/.env << EOF
C2_HOST=127.0.0.1
C2_PORT=9999
CALLBACK_HOST=192.168.56.101        # ← CHANGE to your host/VM IP
CALLBACK_PORT=4444
GPU_IP=127.0.0.1                    # ← your Ollama/GPU machine IP
OLLAMA_HOST=127.0.0.1
EOF


cd Orchestrator
python3 live_orchestrator_backend.py
cd Orchestrator
python3 autonomous_orchestrator.py

# Lab password used by demo agents (SQL Harvester, SSH Tunneler, Metasploit Bridge, etc.)
LAB_PASSWORD=change_me_in_.env     # ← Change this to your own secure password

Disclaimer

This is educational/research code for learning offensive security concepts. Not for unauthorized use. The goal is understanding defenses by building what they defend against.

