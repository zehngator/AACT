import ollama
import subprocess
import time

def query_ollama(prompt):
    """ Sends a prompt to Ollama and gets a response """
    response = ollama.chat(model='dolphin-mistral', 
                           messages=[{"role": "system", "content": prompt}])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
    return response['message']['content']

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
    print(response['message']['tool_calls'])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
    return response['message']['tool_calls']

def extract_code(mess):
    start = mess.find("```")
    print(start)
    #codetype = mess[start+3:].split()[0]
    code = mess[start+3:]
    end = code.find("```")
    code = code[:end-1]
    return code


def run_terminal():
    """ Opens a new interactive terminal and lets Ollama control it """
    
    # Open a new interactive bash shell
    term = subprocess.Popen(["gnome-terminal", "--", "bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    
    print("[+] Terminal opened. Waiting for Ollama's commands...")

    # Initial problem description
    problem_description = "Solve a ctf at the ip 10.10.10.245"
    #next_command = query_ollama(f"{problem_description} Suggest the first command.")
    next_command = tool_ollama(f"{problem_description} Suggest the first command.")

    count = 0
    # def run_bash(code):
    #     # Send command to terminal
    #     term.stdin.write(next_command + "\n")
    #     term.stdin.flush()
    
    # def run_python(code):
    #     name = str(count)+'.py'
    #     with open(name,"w") as f:
    #         f.write(code)
    #     print(f"[+] created python code under {name}")
    #     count += 1


    while True:
        #command_set = extract_code(next_command)
        print(type(next_command))
        #print(next_command[0]['name'])
        print(next_command[0].function['arguments']['code'])
        
        command_set = next_command[0]['function']['arguments']['code']
        print(f"[+] Ollama suggests: {command_set}")

        # if command_set[0] == 'bash':
        #     run_bash(command_set[1])
        
        # if command_set[0] == 'python':
        #     run_python(command_set[1])
        #     command_set[1] += f"\n This code was saved under {count}.py"
        
        term.stdin.write(command_set + "\n")
        term.stdin.flush()
        # Give the command time to execute
        time.sleep(2)

        # Read the output from the terminal
        output = term.stdout.read()
        if not output:
            print("[!] No output received.")
            output = "no output recived"

        print(f"[+] Command Output:\n{output}")

        # Ask Ollama to decide the next step based on output
        next_command = query_ollama(f"The last command was:\n{command_set}\nThe output was:\n{output}\nWhat is the next command?")
        
        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

    term.stdin.write("exit\n")
    term.stdin.flush()
    term.terminate()
    print("[+] Terminal session closed.")

if __name__ == "__main__":
    run_terminal()
