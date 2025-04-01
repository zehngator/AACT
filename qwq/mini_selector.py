
import ollama 

def selector(messages, last_response):
    """ Sends a prompt to Ollama and gets a response """
    #print(prompt)
    prompt = f"The last command that was executed was:\n {messages}\n The" \
             f" response from the terminal was:\n{last_response}\n has the command finsihed excuting or does it need more time?"
    messages = [{"role": "system",
                 "content": "Your job is to determine if the command has finished running or if it needs more time to run. and you need to always use command_complete."
                 },
        {"role": "user", 
         "content": prompt,
        }]
    get_status = [{
                    'type': "function",
                    'function': {
                        'name': 'finish determiner',
                        'description': 'decides weather or not the command has finished running',
                        'parameters' : {
                            'type': 'object',
                            'properties': {
                                "command_complete" : {
                                    "type": "boolean",
                                    "description": "Has the given command finished running and is the cmdline wait for response? ei Cmdline waiting for more input = true : still processing the command = False"
                                },
                                "expected_commandtype" :{
                                    "type": "string",
                                    "description": "What type of command is expected to come next? ie. bash, redis, etc."
                                },
                                "why" : {
                                    "type": "string",
                                    "description": "The reason for the choosing that code"
                                }
                            },
                            'required': ['run_status', 'expected_commandtype']
                        }
                    }
                }]
    response = ollama.chat(model="llama3.1:8b", 
                           messages=messages,
                           tools=get_status
                           )
    print(response)
    broken_up = response['message']['tool_calls'][0]['function']['arguments']
    finished = broken_up['command_complete']
    expected_command = broken_up['expected_commandtype']
    return (finished, expected_command)

if __name__ == "__main__":
    import subprocess
    sig_name = "พ"
    output = subprocess.run(f"tmux capture-pane -p -t _ctf", shell=True, capture_output=True, text=True).stdout
    output = output[output.rfind(sig_name) + len(sig_name):].strip()
    messages = "nmap -p- -T4 -sV 10.129.76.188"
    last_response = "total 0"
    print(output)
    print(selector(messages, output)) 