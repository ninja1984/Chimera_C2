#!/usr/bin/env python3
import socket, threading, json

HOST, PORT = '127.0.0.1', 9999

class SecurityKnowledgeGraph:
    def __init__(self):
        # === SIMULATION BOUNDARY ===
        # The true property-based architecture of the isolated network map
        self.graph = {
            "nodes": {
                "node_1": {
                    "name": "LOCAL_KALI_STAGING",
                    "interfaces": ["192.168.56.104"],
                    "accessible_networks": ["192.168.56.0/24"],
                    "status": "COMPROMISED"
                },
                "node_2": {
                    "name": "METASPLOITABLE_GATEWAY",
                    "interfaces": ["192.168.56.189", "10.0.0.2"],
                    "accessible_networks": ["192.168.56.0/24", "10.0.0.0/24"],
                    "services": {"21/tcp": "vsftpd 2.3.4"},
                    "verified_vulnerabilities": ["CVE-2011-2523"],
                    "status": "DISCOVERED"
                },
                "node_3": {
                    "name": "INTERNAL_DOMAIN_CONTROLLER",
                    "interfaces": ["10.0.0.5"],
                    "accessible_networks": ["10.0.0.0/24"],
                    "services": {"22/tcp": "OpenSSH 8.4p1"},
                    "verified_vulnerabilities": ["Misconfigured SSH Key"],
                    "status": "HIDDEN"
                }
            }
        }
        # ===========================

    def get_view_for_ai(self):
        visible_nodes = {}
        for nid, data in self.graph["nodes"].items():
            if data["status"] in ["COMPROMISED", "DISCOVERED"]:
                visible_nodes[nid] = {
                    "name": data["name"],
                    "interfaces": data["interfaces"],
                    "status": data["status"]
                }
                if data["status"] == "COMPROMISED" and "accessible_networks" in data:
                    visible_nodes[nid]["accessible_networks"] = data["accessible_networks"]
                if "services" in data:
                    visible_nodes[nid]["services"] = data["services"]
        return {"discovered_topology": visible_nodes}

    def execute_action(self, cmd, args):
        parts = args.split()
        
        if cmd == "nodes":
            return json.dumps(self.get_view_for_ai(), indent=2)

        elif cmd == "analyze":
            target_ip = parts[0] if parts else ""
            for nid, data in self.graph["nodes"].items():
                if target_ip in data["interfaces"]:
                    if data["status"] == "DISCOVERED":
                        can_reach = False
                        for cid, cdata in self.graph["nodes"].items():
                            if cdata["status"] == "COMPROMISED":
                                if any(net.split('.')[0:2] == target_ip.split('.')[0:2] for net in cdata["accessible_networks"]):
                                    can_reach = True
                        if can_reach:
                            data["status"] = "COMPROMISED"
                            for h_id, h_data in self.graph["nodes"].items():
                                if h_data["status"] == "HIDDEN" and any(net in data["accessible_networks"] for net in h_data["accessible_networks"]):
                                    h_data["status"] = "DISCOVERED"
                            return f"[+] Graph State Updated: {target_ip} verified, access token stored, session state escalated to COMPROMISED."
                        return "[-] Validation Error: Target host is structurally unreachable from any current foothold network."
                    elif data["status"] == "COMPROMISED":
                        return f"[*] Graph Notice: Node {target_ip} is already fully analyzed and compromised."
            return f"[-] Graph Routing Failure: Host {target_ip} down or unrecognized."

        elif cmd == "task":
            node_num = parts[0] if len(parts) > 0 else ""
            bash_cmd = " ".join(parts[1:]) if len(parts) > 1 else ""
            node_key = f"node_{node_num}"
            
            if node_key not in self.graph["nodes"] or self.graph["nodes"][node_key]["status"] != "COMPROMISED":
                return f"[-] Graph Execution Error: Command rejected. Node_{node_num} is unauthorized or disconnected."

            current_node = self.graph["nodes"][node_key]
            if "nmap" in bash_cmd:
                target_subnet = bash_cmd.split()[-1]
                if target_subnet not in current_node["accessible_networks"]:
                    return f"[-] Network Error: Interface on Node_{node_num} has no physical route to network range {target_subnet}."
                
                scan_output = f"Starting dynamic scan from Node_{node_num} onto network {target_subnet}...\n"
                found = False
                for t_id, t_data in self.graph["nodes"].items():
                    if t_id != node_key and any(net == target_subnet for net in t_data["accessible_networks"]):
                        t_data["status"] = "DISCOVERED"
                        scan_output += f"-> Found Host: {t_data['interfaces'][0]} | Configured Services: {json.dumps(t_data.get('services', {}))}\n"
                        found = True
                if not found: scan_output += "Scan completed. No active responsive hosts discovered."
                return scan_output

            elif "route" in bash_cmd or "ip a" in bash_cmd:
                return f"Active Operating System Interfaces for {current_node['name']}:\n" + "\n".join([f"  - Adapter: {ip}" for ip in current_node["interfaces"]])

            elif "chimera_utility.sh" in bash_cmd:
                if node_key == "node_3":
                    return "[+] Validation utility executed on primary internal server.\n[+] Analysis logged.\n[+] MISSION ACCOMPLISHED"
                return f"Executing basic utility on {current_node['name']}: tracking active process trees cleanly."
            
            return f"Execution tracking completed for command '{bash_cmd}' on node {node_num}."

        return "[-] System Engine Exception: Unknown network primitive."

skg = SecurityKnowledgeGraph()

def client_handler(cs):
    try:
        raw_request = cs.recv(4096).decode('utf-8').strip()
        if not raw_request: return
        parts = raw_request.split()
        cmd = parts[0].lower()
        args = " ".join(parts[1:])
        
        execution_result = skg.execute_action(cmd, args)
        cs.sendall(execution_result.encode('utf-8'))
    except Exception as e:
        try: cs.sendall(f"[-] Backend Processing Error: {e}".encode('utf-8'))
        except: pass
    finally:
        cs.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    print(f"[*] Graph-Based Automation Network Engine Listening on {HOST}:{PORT}")
    while True:
        c, a = s.accept()
        threading.Thread(target=client_handler, args=(c,)).start()

if __name__ == "__main__":
    main()
