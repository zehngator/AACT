import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import re
import random
from difflib import SequenceMatcher

# --- Settings ---
folder_path = "/home/matt/Desktop/AACT/qwq/ctflogs"
similarity_threshold = 0.75
level_spacing = 2.0    # vertical distance between retry levels
child_offset = 2.0     # horizontal spacing between retries
horizontal_spacing = 12.0  # between root trees

# --- Functions ---
def extract_base_command(cmd):
    try:
        return cmd.strip().split()[0]
    except Exception:
        return None

def clean_command(cmd):
    return cmd.strip().lower()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def split_command_label(cmd, max_line_length=15, max_total_length=50):
    if len(cmd) > max_total_length:
        cmd = cmd[:max_total_length] + "..."
    parts = cmd.split()
    wrapped_parts = []
    for part in parts:
        while len(part) > max_line_length:
            wrapped_parts.append(part[:max_line_length])
            part = part[max_line_length:]
        wrapped_parts.append(part)
    return "\n".join(wrapped_parts)

# --- Load Commands ---
all_commands = []

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path)
            if df.empty or 'command' not in df.columns:
                continue
            base_commands = df['command'].dropna().tolist()
            all_commands.extend(base_commands)
        except Exception as e:
            print(f"Skipping {filename}: {e}")

# --- Group Commands into Retry Chains ---
retry_chains = []
current_chain = []

for i, cmd in enumerate(all_commands):
    cmd_clean = clean_command(cmd)
    if not current_chain:
        current_chain.append(cmd_clean)
    else:
        last_cmd = current_chain[-1]
        if extract_base_command(cmd_clean) == extract_base_command(last_cmd) and similar(cmd_clean, last_cmd) > similarity_threshold:
            current_chain.append(cmd_clean)
        else:
            retry_chains.append(current_chain)
            current_chain = [cmd_clean]

if current_chain:
    retry_chains.append(current_chain)

# --- Build Graph ---
G = nx.DiGraph()

for chain in retry_chains:
    for i in range(len(chain)):
        node_label = split_command_label(chain[i])
        if i < len(chain) - 1:
            next_label = split_command_label(chain[i+1])
            G.add_edge(node_label, next_label)

# --- Create Fan-Out Layout ---
pos = {}
x_offset = 0

roots = [n for n in G.nodes if G.in_degree(n) == 0]

for root in roots:
    stack = [(root, x_offset, 0)]  # (node, x, y)
    visited = set()

    while stack:
        node, x, y = stack.pop(0)
        if node in visited:
            continue
        visited.add(node)
        pos[node] = (x, -y)

        children = list(G.successors(node))
        num_children = len(children)

        if num_children == 1:
            # Single child → place straight down
            stack.append((children[0], x, y + level_spacing))
        elif num_children > 1:
            # Multiple children → fan out left and right
            start_x = x - child_offset * (num_children - 1) / 2
            for i, child in enumerate(children):
                child_x = start_x + i * child_offset
                child_y = y + level_spacing
                stack.append((child, child_x, child_y))
    x_offset += horizontal_spacing  # Move next root tree over

# Assign random position if missing
for node in G.nodes():
    if node not in pos:
        pos[node] = (random.uniform(-10, 10), random.uniform(-10, 10))

# --- Draw Final Fan-Out Graph ---
node_colors = []
for node in G.nodes():
    if G.out_degree(node) > 0:
        node_colors.append("red")    # Retry node
    else:
        node_colors.append("green")  # Success node

plt.figure(figsize=(32, 24))
nx.draw(G, pos,
        with_labels=True,
        node_size=3000,
        node_color=node_colors,
        font_size=6,
        font_weight="bold",
        arrows=True,
        arrowsize=20)

plt.title("CTF Retry Attempts (Fan-Out Layout, Small Font)", fontsize=20)
plt.axis('off')

plt.savefig("/home/matt/Desktop/AACT/qwq/ctf_retries.png", format="png", dpi=300, bbox_inches='tight')
print("Graph saved to /home/matt/Desktop/AACT/qwq/ctf_retries.png")
plt.show()