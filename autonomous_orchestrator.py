#!/usr/bin/env python3
import socket, json, urllib.request, time, os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

GPU_IP = os.getenv("GPU_IP", "127.0.0.1")
OLLAMA_API = f"http://{GPU_IP}:11434/api/generate"

HANDLER_MODEL = "llama3:latest"
ANALYST_MODEL = "llama3:latest"

console = Console()
graph_state = {}
huddle_log = ["[dim]Awaiting multi-agent consultation...[/dim]"]
execution_log = ["[dim]System Initialized. Awaiting intelligence loop...[/dim]"]
current_cycle = 0
max_cycles = 20
current_status = "[bold yellow]INITIALIZING[/]"

def generate_graph_table():
    table = Table(title="Live Topology Graph", expand=True, style="cyan")
    table.add_column("Node ID", style="bold blue")
    table.add_column("Interfaces", style="green")
    table.add_column("Status", style="bold magenta")
    if not graph_state: table.add_row("N/A", "Awaiting Discovery...", "BLIND")
    else:
        for nid, data in graph_state.items():
            table.add_row(nid, ", ".join(data.get("interfaces", [])), data.get("status", "UNKNOWN"))
    return table

def generate_layout():
    layout = Layout(name="root")
    layout.split(Layout(name="header", size=3), Layout(name="main", ratio=1), Layout(name="footer", size=10))
    layout["main"].split_row(Layout(name="left", ratio=1), Layout(name="right", ratio=1))
    
    # THE COLOR GLITCH FIX
    header_text = f"[bold white]CHIMERA C2 | CYCLE: {current_cycle}/{max_cycles} | STATUS: {current_status}[/]"
    layout["header"].update(Panel(header_text, style="on blue", subtitle="[Agent Framework]"))
    
    layout["left"].update(Panel(generate_graph_table(), border_style="cyan"))
    layout["right"].update(Panel("\n\n".join(huddle_log[-4:]), title="[bold yellow]Tactical Huddle[/]", border_style="yellow"))
    layout["footer"].update(Panel("\n".join(execution_log[-8:]), title="[bold green]Raw Execution Feed[/]", border_style="green"))
    return layout

def log_exec(msg): execution_log.append(msg)

def send_to_backend(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9999))
        s.sendall(command.encode('utf-8'))
        response = s.recv(8192).decode('utf-8')
        s.close()
        return response
    except: return "[-] FATAL: Graph validation engine offline."

def ask_api(prompt, model, temp=0.0, force_json=False):
    data = {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temp}}
    if force_json: data["format"] = "json"
    req = urllib.request.Request(OLLAMA_API, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode()).get("response", "{}").strip()
    except Exception as e: return f"[-] API Error: {e}"

def run_loop():
    global current_cycle, current_status, graph_state
    rules = (
        "OBJECTIVE: Evaluate the network graph and establish full verification connectivity.\n"
        "AVAILABLE OPERATIONS: ['nodes', 'analyze [IP]', 'task [NODE_NUM] [BASH_CMD]', 'consult [QUESTION]']\n\n"
        "REASONING CONSTRAINTS:\n"
        "1. Start with 'nodes'.\n"
        "2. Use 'analyze [IP]' on discovered assets to verify access. YOU MUST USE THE IP ADDRESS, NOT THE NODE NAME.\n"
        "OUTPUT EXACTLY IN THIS JSON FORMAT:\n"
        "{\"thought\": \"your reasoning\", \"action\": \"your command\"}"
    )
    history = rules + "\n[!] SYSTEM ACTIVE.\n"
    
    with Live(generate_layout(), refresh_per_second=4, screen=True) as live:
        for cycle in range(1, max_cycles + 1):
            current_cycle = cycle
            current_status = "[bold yellow]THINKING...[/]"
            live.update(generate_layout())
            
            resp = ask_api(history + "\nCHOOSE NEXT ACTION:", HANDLER_MODEL, force_json=True)
            
            try:
                ai = json.loads(resp)
                thought = ai.get("thought", "N/A")
                action = str(ai.get("action", ""))
            except:
                thought = "[FORMAT ERROR] AI sent raw text instead of JSON."
                action = resp.replace("\n", " ")[:50]
                
            log_exec(f"[bold blue][Llama 3][/] {thought}")
            log_exec(f"[bold magenta][Proposed Action][/] {action}")
            
            current_status = "[bold red]AWAITING OPERATOR INPUT[/]"
            live.update(generate_layout())
            live.stop() 
            user_choice = console.input("\n[bold red]oracle@chimera:~# Authorize AI action? (y/n, or type override command): [/]").strip()
            live.start() 
            
            if user_choice.lower() == 'n':
                log_exec("[bold red][-] Execution Blocked by Operator.[/]")
                history += f"\nOPERATOR OVERRIDE: Blocked '{action}'."
                continue
            elif user_choice.lower() != 'y' and user_choice != '':
                log_exec(f"[bold yellow][!] Injecting Human Override:[/] {user_choice}")
                history += f"\nSYSTEM ERROR ON PREVIOUS ACTION. OPERATOR SAYS: {user_choice}"
                continue
            
            current_status = "[bold cyan]EXECUTING ACTION[/]"
            live.update(generate_layout())
            parts = action.split()
            base = parts[0].lower() if parts else ""
            
            if base == "consult":
                question = " ".join(parts[1:])
                huddle_log.append(f"[bold cyan][Llama 3][/] {question}")
                live.update(generate_layout())
                advisor_reply = ask_api(f"You are a Red Team advisor. The AI Coordinator asks: {question}", ANALYST_MODEL, temp=0.4)
                huddle_log.append(f"[bold magenta][Neo][/] {advisor_reply}")
                history += f"\nACTION: {action}\nADVISOR RESPONSE: {advisor_reply}"
                time.sleep(2.0)
                continue
                
            res = send_to_backend(action)
            log_exec(f"[green]{res.strip()}[/green]")
            history += f"\nACTION: {action}\nRESULT: {res.strip()}"
            
            # THE NODE 3 STATE PATCH
            if base == "nodes":
                try: graph_state = json.loads(res).get("discovered_topology", {})
                except: pass
            
            # Force the UI to update if the attack was successful
            if "escalated to COMPROMISED" in res:
                target_ip = parts[1] if len(parts) > 1 else ""
                for nid, data in graph_state.items():
                    if target_ip in data.get("interfaces", []):
                        graph_state[nid]["status"] = "COMPROMISED"
            
            time.sleep(1.0)

if __name__ == "__main__":
    run_loop()
