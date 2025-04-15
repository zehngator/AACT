import subprocess
session_name = "_ctf"
sig_name = "ctf"
ip_address =''
tool_ollama = ''
next_command = ''
why = ''
output = ''

# a: creating the message along with the AI's purpose
start_message= [{'role': "system", 'content': f"You are a ctf solver and you are given a task to \
                 solve a ctf at the IP {ip_address} and you need to use the extract_code tool \
                    everytime. To reiterate you must use the tool call no matter what even if it is a bad code."}]
# b: Inital call to AI to solve the ctf
full_command, messages = tool_ollama(start_message, f"{problem_description} Suggest the first command to solve the ctf .")
# c: Feeding results back to the AI
messages.append({'role': "assistant", 'content': f"Ollama suggested {next_command} because {why}"})
messages.append({'role': "system", 'content': f"Executed {next_command} : Results: {output}"})
# d: Requerying the AI for the next command
full_command, messages = tool_ollama(messages, f"What is the next step to solve the ctf?")

# a: Calling commands through a tmux session
if Timed_out:
    subprocess.run(f"tmux send-keys -t {session_name} \"{next_command}\" C-m", shell=True)
else:
    subprocess.run(f"tmux send-keys -t {session_name} '{next_command}; tmux wait-for -S {sig_name}' C-m", shell=True)
# b: Captuing the output of the command through tmux
output = subprocess.run(f"tmux capture-pane -p -t {session_name}", shell=True, capture_output=True, text=True).stdout
# c: IO blocking using tmux signals
def wait_response(sig_name, mess):
    global Timed_out
    try:
        subprocess.run(f"tmux wait-for {sig_name}", shell=True,timeout=30)
        Timed_out = False
    except subprocess.TimeoutExpired:
        Timed_out = True
        print("[+] Command took too long to execute. Moving on to the next command.")
        