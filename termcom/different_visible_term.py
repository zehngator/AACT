import ollama
import subprocess
import time

def query_ollama(prompt):
    """ Sends a prompt to Ollama and gets a response """
    response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def extract_code(mess):
    start = mess.find("'''")
    codetype = mess[:start].split()[-1]
    code = mess[start+3:]
    end = code.find("'''")
    code = code[:end]
    return [codetype,code]


def run_terminal():
    """ Opens a new interactive terminal and lets Ollama control it """
    
    # Open a new interactive bash shell
    term = subprocess.Popen(["gnome-terminal", "--", "bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    
    print("[+] Terminal opened. Waiting for Ollama's commands...")

    # Initial problem description
    problem_description = "This is a CTF challenge where you must analyze a system using Linux commands. Start by gathering information."
    next_command = query_ollama(f"{problem_description} Suggest the first command.")

    count = 0
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


    while True:
        command_set = extract_code(next_command)
        print(f"[+] Ollama suggests: {command_set}")

        if command_set[0] == 'bash':
            run_bash(command_set[1])
        
        if command_set[0] == 'python':
            run_python(command_set[1])
            command_set[1] += f"\n This code was saved under {count}.py"
        
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
