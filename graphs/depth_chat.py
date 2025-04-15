import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import re
from collections import Counter

# Final custom MITRE mapping based on your real commands
custom_mitre_mapping = {
    "nmap": "Reconnaissance (Active Scanning)",
    "curl": "Command and Control (Ingress Tool Transfer)",
    "import": "Execution (Command and Scripting Interpreter)",
    "smbclient": "Discovery (Remote System Discovery)",
    "nc": "Command and Control (Remote Access Tools)",
    "unzip": "Collection (Archive Collected Data)",
    "cat": "Collection (Local Data Access)",
    "echo": "Execution (Shell Command)",
    "ftp": "Initial Access (Exploit Public-Facing Application)",
    "get": "Collection (Data from Information Repositories)",
    "sudo": "Privilege Escalation (Abuse Elevation Control Mechanism)",
    "crackmapexec": "Credential Access (Brute Force / Discovery)",
    "anonymous": "Credential Access (Valid Accounts)",
    "ls": "Discovery (File and Directory Discovery)",
    "exit": "Other",
    "dir": "Discovery (File and Directory Discovery)",
    "mono": "Execution (Command and Scripting Interpreter)",
    "USER": "Credential Access (Valid Accounts)",
    "fcrackzip": "Credential Access (Password Cracking)"
}

# Function to extract the base command
def extract_base_command(cmd):
    try:
        return cmd.strip().split()[0]
    except Exception:
        return None

# Function to map command to MITRE tactic
def map_to_mitre(command):
    command_lower = command.lower()
    for keyword, tactic in custom_mitre_mapping.items():
        if keyword.lower() in command_lower:
            return tactic
    return "Other"

# Function to extract main name without trailing numbers
def extract_main_name(filename):
    return re.sub(r'_[0-9]+\.csv$', '', filename)

# Path to the folder containing your CSV files
folder_path = "/home/matt/Desktop/AACT/qwq/ctflogs/Achetype"

# Aggregate all tactics from all CSVs, track their grouped main name
all_tactics_sequence = []

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path)
            if df.empty or 'command' not in df.columns:
                continue
            base_commands = df['command'].dropna().apply(extract_base_command)
            tactics = base_commands.apply(map_to_mitre)
            # Remove consecutive duplicates
            tactics = tactics[tactics != tactics.shift()].tolist()
            # Record tactics with their grouped main file name
            main_name = extract_main_name(filename)
            for tactic in tactics:
                if tactic != "Other":
                    all_tactics_sequence.append((tactic, main_name))
        except Exception as e:
            print(f"Skipping {filename}: {e}")

# Build the overall graph with labels showing main name
G = nx.DiGraph()
for i in range(len(all_tactics_sequence) - 1):
    (src_tactic, src_group) = all_tactics_sequence[i]
    (dst_tactic, dst_group) = all_tactics_sequence[i + 1]
    G.add_edge(f"{src_tactic}\n[{src_group}]", f"{dst_tactic}\n[{dst_group}]")

# Draw the unified depth graph
plt.figure(figsize=(24, 14))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True, node_size=3500, node_color="lightblue", font_size=8, font_weight="bold", arrowsize=20)
plt.title("Unified CTF MITRE ATT&CK Depth Graph (Grouped by Main File Name)", fontsize=16)
plt.show()
