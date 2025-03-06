import ollama 
import subprocess
import os
import csv
from pathlib import Path


def createUniqueLog(filename, directory="/home/matt/Desktop/AACT/termcom/ctflogs"):
    counter = 1 
    while True:
        file = Path(directory) / f"{filename}_{counter}.csv"
        if not os.path.exists(file):
            with file.open('w', newline='') as f:
                info = ["command number", "command", "reasoning", "output"]
                writer = csv.writer(f)
                writer.writerow(info)
                # f.write(f"This is instance log #{counter} of {filename}\n")
                # f.write("command number, command,reasoning, output ")
                print(f"[+] File create: {filename}")
            return file
        counter += 1


def tool_ollama(prompt):
    """ Sends a prompt to Ollama and gets a response """
    #print(prompt)
    message = [
        {"role": "user", 
         "content": prompt,
        #  },
        # {'role': "system", 
        #  'content': "You are a ctf solver and you are given a task to solve a ctf at the IP and you need to use the extract_code tool everytime"
        }]
    get_code = [{
                    'type': "function",
                    'function': {
                        'name': 'extract_code',
                        'description': 'provides the next command to run',
                        'parameters' : {
                            'type': 'object',
                            'properties': {
                                "code_type" : {
                                    "type": "string",
                                    "description": "The type of code that is getting extract"
                                },
                                "code" :{
                                    "type": "string",
                                    "description": "The code that is getting extract"
                                },
                                "why" : {
                                    "type": "string",
                                    "description": "The reason for the choosing that code"
                                }
                            },
                            'required': ['code_type', 'code']
                        }
                    }
                }]
    response = ollama.chat(model='llama3.1:8b', 
                           messages=message,
                           tools=get_code
                           )
    #print(response['message']['tool_calls'])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
        #print(response['message']['content'])
    print(response)
    return response['message']['tool_calls']

problem_description = "Solve a ctf at the IP 10.129.91.189 using redis-cli"
ip_address ="10.129.91.189"

def wait_response(sig_name):
    try:
        subprocess.run(f"tmux wait-for {sig_name}", shell=True,timeout=30)
    except subprocess.TimeoutExpired:
        print("[+] Command took too long to execute. Moving on to the next command.")

def run_terminal():
    """ Opens a persistent tmux session and executes commands inside it """
    
    # Start a tmux session
    session_name = "ollama_ctf"
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
    print("[+] tmux session started. Running commands inside it.")

    #create log file 
    file = createUniqueLog("Redeemerp2")
    #problem_description = "Solve a ctf at the IP 10.129.91.189"
    full_command = tool_ollama(f"{problem_description} Suggest the first command to solve the ctf .")
    sig_name = "พ"

    # counter for logging which command it is
    counter = 1
    while True:

        ########################### Isolating variabes from llama ###############################
        broken_up = full_command[0]['function']['arguments']
        next_command = broken_up['code']
        why = ''
        if broken_up['why']:
            why = broken_up['why']
        ##########################################################################################

        print(f"[+] Ollama suggests: {next_command}")
        # if (full_command[0]['function']['arguments']['why']):
        #     print(full_command[0]['function']['arguments']['why'])
        # Run command inside tmux session
        subprocess.run(f"tmux send-keys -t {session_name} '{next_command}; tmux wait-for -S {sig_name}' C-m", shell=True)
        wait_response(sig_name)
        # Simulate waiting for command execution
        output = subprocess.run(f"tmux capture-pane -p -t {session_name}", shell=True, capture_output=True, text=True).stdout
        with file.open('a',newline='') as f:
            instance = [counter , next_command , why , output[output.rfind(sig_name)+len(sig_name):].strip()]
            writer = csv.writer(f,quoting=csv.QUOTE_ALL)
            writer.writerow(instance)
            counter += 1

        output = output[output.rfind(sig_name) + len(sig_name):]
        print(f"[+] Command Output:\n{output}")

        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

        full_command = tool_ollama(f"The last command was: {next_command} The output was: {output}\nWhat is the next command to solve the ctf at this ip {ip_address}?")

    # Close tmux session
    subprocess.run(f"tmux kill-session -t {session_name}", shell=True)
    print("[+] tmux session closed.")



if __name__ == "__main__":
    run_terminal()
