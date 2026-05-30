# Chimera C2 Framework

A from-scratch red team C2 framework built to understand implant development and create signature-free tooling.

## Purpose

Deep-dive learning project into C2 architecture, from kernel-level agents to AI-orchestrated command and control. Built to understand how modern adversarial platforms work at every layer rather than relying on existing (heavily signatured) tools.

## What This Demonstrates

- Custom C2 infrastructure design (Python orchestrator + C kernel agents)
- Multi-tier attack chain architecture (recon to exploitation to persistence to exfiltration)
- AI/LLM integration for autonomous operation reasoning
- 300+ experimental modules covering offensive security techniques
- Signature-free tooling approach

## Repository Structure

- Agents: Experimental attack modules (Python/C)
- Orchestrator: C2 server with AI integration
- Vanguard: Tactical strike modules
- Tier2_C_Agents: Kernel-level components (C)
- config: Environment-based configuration
- tests: Unit tests (sparse, research focus)

## Quick Start

Prerequisites: Python 3.8+, Ollama, Linux environment

Installation:
    git clone https://github.com/ninja1984/Chimera_C2.git
    cd Chimera_C2
    pip install -r requirements.txt

Configuration:
    cp config/.env.example config/.env
    Edit config/.env with your lab settings
    source config/.env
    python3 Orchestrator/autonomous_orchestrator.py

## Background

Self-directed 12-month intensive study in offensive security engineering. Focus on understanding C2 internals rather than using off-the-shelf tools. Experimental codebase, research quality, not production-hardened.

## Security

Strictly for authorized security research. Isolated lab environments only.

## License

MIT License
