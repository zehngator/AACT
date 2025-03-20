
import ollama 

def selector(messages, last_response):
    """ Sends a prompt to Ollama and gets a response """
    #print(prompt)
    prompt = f"The last command that was executed was:\n {last_response}\n The" \
             f" response from the terminal was:\n{last_response}\n has the command finsihed excuting or does it need more time?"
    messages = [{"role": "user", 
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
                                "run_status" : {
                                    "type": "boolean",
                                    "description": "Has the given command finished running and is ready for the next command?"
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
    response = ollama.chat(model="llama3.2:1b", 
                           messages=messages,
                           tools=get_status
                           )
    print(response)
    broken_up = response['message']['tool_calls'][0]['function']['arguments']
    finished = broken_up['run_status']
    expected_command = broken_up['expected_commandtype']
    return (finished, expected_command)
    