#code I may need later but is getting cut from main code for better clearity 

#Code to run diffrenet stuff based on what type of code is given
def run_bash(code):
        # Send command to terminal
        term.stdin.write(next_command + "\n")
        term.stdin.flush()
    
def run_python(code):
        name = str(count)+'.py'
        with open(name,"w") as f:
            f.write(code)
        print(f"[+] created python code under {name}")
        count += 1

if command_set[0] == 'bash':
    run_bash(command_set[1])

if command_set[0] == 'python':
    run_python(command_set[1])
    command_set[1] += f"\n This code was saved under {count}.py"


###########################################################

# Using llama with message content instead of tool_calls
def query_ollama(prompt):
    """ Sends a prompt to Ollama and gets a response """
    response = ollama.chat(model='dolphin-mistral', 
                           messages=[{"role": "system", "content": prompt}])
    with open('last_response.txt', "w") as f:
        f.write(response['message']['content'])
    return response['message']['content']

def extract_code(mess):
    start = mess.find("```")
    print(start)
    #codetype = mess[start+3:].split()[0]
    code = mess[start+3:]
    end = code.find("```")
    code = code[:end-1]
    return code

###########################################################

# Running terminal using popen

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
    


    while True:
        #command_set = extract_code(next_command)
        # print(type(next_command))
        #print(next_command[0]['name'])

        print(next_command[0].function['arguments']['code'])
        
        command_set = next_command[0]['function']['arguments']['code']
        print(f"[+] Ollama suggests: {command_set}")

        if term.stdin:
            print(term.stdin)
            term.stdin.write(command_set + "\n")
            term.stdin.flush()
        else:
            print("[!] Broken pipe detected. Exiting...")
            break
        
        # Give the command time to execute
        time.sleep(2)

        # Read the output from the terminal
        output = term.stdout.read()
        if not output:
            print("[!] No output received.")
            output = "no output recived"

        print(f"[+] Command Output:\n{output}")

        # Ask Ollama to decide the next step based on output
        next_command = tool_ollama(f"The last command was:\n{command_set}\nThe output was:\n{output}\nWhat is the next command?")
        
        if "exit" in next_command.lower():
            print("[+] Ollama decided to stop.")
            break

    term.stdin.write("exit\n")
    term.stdin.flush()
    term.terminate()
    print("[+] Terminal session closed.")