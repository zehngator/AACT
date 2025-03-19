import ollama 
import subprocess
import os
import csv
import time
from pathlib import Path
import argparse


ollama_model = "qwq"
ip_address ="10.129.88.225"
problem_description = f"Solve a ctf at the IP {ip_address}" 
start_message= [{'role': "system", 'content': f"You are a ctf solver and you are given a task to solve a ctf at the IP {ip_address} and you need to use the extract_code tool everytime"}]
Timed_out = False

# Command line arguments
parser = argparse.ArgumentParser(description="Example script with options")
parser.add_argument("-i", "--ip", dest="ip_address", help="IP address of the CTF")
parser.add_argument("-m", "--model", dest="ollama_model", help="Ollama model to use")
parser.add_argument("-d", "--description", dest="problem_description", help="Description of the problem")

args = parser.parse_args()

if args.ip_address:
    ip_address = args.ip_address

if args.ollama_model:
    ollama_model = args.ollama_model

if args.problem_description:
    problem_description = args.problem_description


def createUniqueLog(filename, directory=f"/home/matt/Desktop/AACT/{ollama_model}/ctflogs"):
    counter = 1 
    while True:
        file = Path(directory) / f"{filename}_{counter}.csv"
        if not os.path.exists(file):
            with file.open('w', newline='') as f:
                info = ["command number", "command", "reasoning", "reasoning time", "output", "command time", "ollama's Memory"]
                writer = csv.writer(f)
                writer.writerow(info)
                # f.write(f"This is instance log #{counter} of {filename}\n")
                # f.write("command number, command,reasoning, output ")
                print(f"[+] File create: {str(file)}")
            return file
        counter += 1


def tool_ollama(messages, prompt):
    """ Sends a prompt to Ollama and gets a response """
    #print(prompt)
    messages.append(
        {"role": "user", 
         "content": prompt,
        })
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
    response = ollama.chat(model=ollama_model, 
                           messages=messages,
                           tools=get_code
                           )
    #print(response['message']['tool_calls'])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
        #print(response['message']['content'])
    print(response)
    # return response['message']['tool_calls']
    return (response['message']['tool_calls'], messages)


def wait_response(sig_name):
    try:
        subprocess.run(f"tmux wait-for {sig_name}", shell=True,timeout=30)
        Timed_out = False
    except subprocess.TimeoutExpired:
        Timed_out = True
        print("[+] Command took too long to execute. Moving on to the next command.")

def run_terminal():
    """ Opens a persistent tmux session and executes commands inside it """
    
    # Start a tmux session
    session_name = f"{ollama_model}_ctf"
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
    print("[+] tmux session started. Running commands inside it.")

    #create log file 
    file = createUniqueLog("Redeemer")
    #problem_description = "Solve a ctf at the IP 10.129.91.189"
    start = time.time()
    full_command, messages = tool_ollama(start_message, f"{problem_description} Suggest the first command to solve the ctf .")
    ollama_time = time.time() - start
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
        start = time.time()
        if Timed_out:
            subprocess.run(f"tmux send-keys -t {session_name} '{next_command}' C-m", shell=True)
        else:
            subprocess.run(f"tmux send-keys -t {session_name} '{next_command}; tmux wait-for -S {sig_name}' C-m", shell=True)
        wait_response(sig_name)
        command_time = time.time() - start
        # Simulate waiting for command execution
        output = subprocess.run(f"tmux capture-pane -p -t {session_name}", shell=True, capture_output=True, text=True).stdout
        output = output[output.rfind(sig_name) + len(sig_name):].strip()

        #################                   creating continous ai chat log                 #################
        messages.append({'role': "assistant", 'content': f"Ollama suggested {next_command} because {why}"})
        messages.append({'role': "system", 'content': f"Executed {next_command} : Results: {output}"})
        ####################################################################################################

        ############################# Logging the command and output ############################
        with file.open('a',newline='') as f:
            instance = [counter , next_command , why , ollama_time, output[output.rfind(sig_name)+len(sig_name):].strip(), command_time, messages]
            writer = csv.writer(f,quoting=csv.QUOTE_ALL)
            writer.writerow(instance)
            counter += 1
        ##########################################################################################

        print(f"[+] Command Output:\n{output}")

        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

        full_command, messages = tool_ollama(messages, f"What is the next step to solve the ctf?")
        #full_command, messages = tool_ollama(messages, f"The last command was: {next_command} The output was: {output}\nWhat is the next command to solve the ctf at this ip {ip_address}?")

    # Close tmux session
    subprocess.run(f"tmux kill-session -t {session_name}", shell=True)
    print("[+] tmux session closed.")



if __name__ == "__main__":

    run_terminal()
