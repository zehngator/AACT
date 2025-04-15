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
folder_path = "/home/matt/Desktop/AACT/qwq/ctflogs"

# Aggregate all tactics from all CSVs, track their grouped main name
all_tactics_sequence = []
frequency_counter = Counter()

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
            main_name = extract_main_name(filename)
            for tactic in tactics:
                if tactic != "Other":
                    all_tactics_sequence.append((tactic, main_name))
                    frequency_counter[tactic] += 1
        except Exception as e:
            print(f"Skipping {filename}: {e}")

# Build a simplified graph
G = nx.DiGraph()

# Track last seen tactic to avoid redundant edges
last_seen = {}

for tactic, group in all_tactics_sequence:
    if tactic not in last_seen:
        last_seen[tactic] = set()

for i in range(len(all_tactics_sequence) - 1):
    src_tactic, _ = all_tactics_sequence[i]
    dst_tactic, _ = all_tactics_sequence[i + 1]
    if dst_tactic not in last_seen[src_tactic]:
        G.add_edge(src_tactic, dst_tactic)
        last_seen[src_tactic].add(dst_tactic)

# Calculate node sizes based on how often each tactic appears
node_sizes = [frequency_counter[tactic] * 500 for tactic in G.nodes()]

# Draw the simplified unified weighted depth graph
plt.figure(figsize=(24, 14))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20)
plt.title("Unified Simplified CTF MITRE ATT&CK Depth Graph (Weighted by Usage)", fontsize=16)
plt.show()
