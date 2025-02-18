import ollama
import subprocess
import time



def tool_ollama(prompt):
    """ Sends a prompt to Ollama and gets a response """
    response = ollama.chat(model='llama3.1:8b', 
                           messages=[{"role": "user", "content": prompt}],
                           tools=[{
                               'type': "function",
                               'function': {
                                   'name': 'extract_code',
                                   'description': 'Extracts code for use on the command line',
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
                                           }
                                       },
                                        'required': ['code_type', 'code']
                                   }
                               }
                           }])
    #print(response['message']['tool_calls'])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
        #print(response['message']['content'])
    return response['message']['tool_calls']



import subprocess

def run_terminal():
    """ Opens a persistent tmux session and executes commands inside it """
    
    # Start a tmux session
    session_name = "ollama_ctf"
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)

    print("[+] tmux session started. Running commands inside it.")

    problem_description = "Solve a ctf at the IP 10.10.10.245"
    full_command = tool_ollama(f"{problem_description} Suggest the first command.")

    while True:
        next_command = full_command[0]['function']['arguments']['code']
        print(f"[+] Ollama suggests: {next_command}")

        # Run command inside tmux session
        subprocess.run(f"tmux send-keys -t {session_name} '{next_command}' Enter", shell=True)

        # Simulate waiting for command execution
        output = subprocess.run(f"tmux capture-pane -p -t {session_name}", shell=True, capture_output=True, text=True).stdout
        print(f"[+] Command Output:\n{output}")

        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

        next_command = tool_ollama(f"The last command was:\n{next_command}\nThe output was:\n{output}\nWhat is the next command?")

    # Close tmux session
    subprocess.run(f"tmux kill-session -t {session_name}", shell=True)
    print("[+] tmux session closed.")



if __name__ == "__main__":
    run_terminal()
