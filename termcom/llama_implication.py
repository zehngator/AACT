import ollama
import groq 
import subprocess
import time
import os

def createUniqueLog(filename):
    counter = 1 
    while True:
        file = f"{filename}{counter}.txt"
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(f"This is instance log #{counter} of {filename}\n")
                print(f"[+] File create: {filename}")
            return filename


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




def run_terminal():
    """ Opens a persistent tmux session and executes commands inside it """
    
    # Start a tmux session
    session_name = "ollama_ctf"
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)

    print("[+] tmux session started. Running commands inside it.")
    filename = createUniqueLog("ctflogs/Redeemer")
    problem_description = "Solve a ctf at the IP 10.129.49.90"
    full_command = tool_ollama(f"{problem_description} Suggest the first command.")
    sig_name = "ioefwj"
    while True:
        next_command = full_command[0]['function']['arguments']['code']
        print(f"[+] Ollama suggests: {next_command}")
        # if (full_command[0]['function']['arguments']['why']):
        #     print(full_command[0]['function']['arguments']['why'])
        # Run command inside tmux session
        subprocess.run(f"tmux send-keys -t {session_name} '{next_command}; tmux wait-for -S {sig_name}' C-m", shell=True)
        subprocess.run(f"tmux wait-for {sig_name}", shell=True)
        # Simulate waiting for command execution
        output = subprocess.run(f"tmux capture-pane -p -t {session_name}", shell=True, capture_output=True, text=True).stdout
        with open(filename, 'a') as f:
            f.write(output[output.rfind('➜'):]+'\n')

        output = output[output.rfind(sig_name) + len(sig_name):]
        print(f"[+] Command Output:\n{output}")

        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

        full_command = tool_ollama(f"The last command was:\n{next_command}\nThe output was:\n{output}\nWhat is the next command?")

    # Close tmux session
    subprocess.run(f"tmux kill-session -t {session_name}", shell=True)
    print("[+] tmux session closed.")



if __name__ == "__main__":
    run_terminal()
