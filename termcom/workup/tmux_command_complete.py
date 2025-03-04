

# import subprocess
# import time

# # Start a tmux session and run a long command
# subprocess.run("tmux new-session -d -s mysession", shell=True)
# subprocess.run("tmux send-keys -t mysession 'nmap -p- -sV 10.129.201.161' Enter", shell=True)

# # Check if the tmux session is still running
# while True:
#     output = subprocess.run("tmux list-panes -t mysession -F '#{pane_active}'", shell=True, capture_output=True, text=True)
#     print(output.stdout)
#     if '1' not in output.stdout:  # Pane is inactive
#         print("Command completed!")
#         break

#     time.sleep(1)  # Poll every second
import subprocess

SESSION_NAME = "nmap_scan"
sig_name = "scan_done"
# Run the command inside a tmux session and notify on completion
tmux_command = f"tmux send-keys -t {SESSION_NAME} 'nmap -p- -sV 10.129.201.161; echo Scan Finished; tmux wait-for -S scan_done' C-m"

subprocess.run(tmux_command, shell=True)

# Wait for the signal
subprocess.run("tmux wait-for scan_done", shell=True)
output = subprocess.run(f"tmux capture-pane -p -t {SESSION_NAME}", shell=True, capture_output=True, text=True).stdout
dist = output.find(sig_name)
print(f"dist ={dist}")
output = output[output.find(sig_name) + len(sig_name):]
print(f"[+] Command Output:\n{output}")
print("Command completed!")

