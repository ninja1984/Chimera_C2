import os
import sys
import subprocess

class Overmind:
    def __init__(self):
        self.root = "/home/dan/Chimera_Project/agents"
        self.categories = {
            "1": ("RECON (0-40)", range(0, 41)),
            "2": ("ACCESS (41-139)", range(41, 140)),
            "3": ("PERSISTENCE (140-169)", range(140, 170)),
            "4": ("SHADOW OPS (170-210)", range(170, 211))
        }

    def display_menu(self):
        os.system('clear')
        print("==============================================")
        print("   CHIMERA PROJECT: MASTER OVERMIND v3.0      ")
        print("   Status: GATED | Agents: 200+ | Phase: III  ")
        print("==============================================")
        for key, (name, _) in self.categories.items():
            print(f" [{key}] {name}")
        print(" [Q] Emergency Quit")
        
        choice = input("\nSelect Operational Phase > ").upper()
        if choice == 'Q': sys.exit()
        if choice in self.categories:
            self.show_category(choice)

    def show_category(self, cat_key):
        name, num_range = self.categories[cat_key]
        print(f"\n--- {name} ---")
        
        found = []
        # Dynamic directory scanning to handle your 500+ folder tree
        all_folders = sorted([f for f in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, f))])
        for folder in all_folders:
            try:
                num = int(folder.split("_")[0])
                if num in num_range:
                    found.append(folder)
            except: continue
            
        for i, agent in enumerate(found):
            print(f" {i:3} | {agent}")
            
        pick = input("\nLaunch ID (or 'B' for Back) > ")
        if pick.upper() == 'B': return
        try:
            self.execute_logic(found[int(pick)])
        except:
            print("Invalid Selection.")

    def execute_logic(self, agent_folder):
        # 170-C GATE: Protect the 20h of research from Agent 187/Omega
        if "187" in agent_folder or "Omega" in agent_folder:
            print("\n[!!!] DESTRUCTIVE AGENT DETECTED [!!!]")
            key = input("ENTER 170-C CRYPTOGRAPHIC KEY TO PROCEED: ")
            if key != "CHIMERA_PRO_2026": # Replace with your actual gated pass
                print("ACCESS DENIED. LOCKING SECTOR.")
                return

        path_py = os.path.join(self.root, agent_folder, "src", "main.py")
        path_exe = os.path.join(self.root, agent_folder, "bin", "agent_201_x64.exe")

        if os.path.exists(path_py):
            subprocess.run(["python3", path_py])
        elif os.path.exists(path_exe):
            print(f"[*] Binary found. Deployment ready for Windows target: {agent_folder}")
        else:
            print(f"[-] No actionable source in {agent_folder}/src/")
        input("\nSequence Complete. Press Enter...")

if __name__ == "__main__":
    om = Overmind()
    while True:
        om.display_menu()
