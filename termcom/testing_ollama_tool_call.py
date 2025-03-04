import ollama

def tool_ollama(prompt):
    """ Sends a prompt to Ollama and gets a fresh response """
    try:
        response = ollama.chat(
            model='ishumilin/deepseek-r1-coder-tools:8b',
            messages=[{"role": "user", "content": prompt}],
            tools=[{
                'type': "function",
                'function': {
                    'name': 'extract_code',
                    'description': 'Extracts code for use on the command line',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            "code_type": {
                                "type": "string",
                                "description": "The type of code that is getting extracted"
                            },
                            "code": {
                                "type": "string",
                                "description": "The code that is getting extracted"
                            }
                        },
                        'required': ['code_type', 'code']
                    }
                }
            }]
        )

        # Check if the response contains tool calls
        if 'tool_calls' in response['message']:
            # with open('last_response.txt', "w") as f:
            #     f.write(response['message']['content'])
            print(f"Tool calls: {response['message']['tool_calls']}")  # Print tool calls to debug
            return response['message']['tool_calls']
        else:
            print("No tool calls found in the response.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Test the function with multiple calls
next_command = "nmap 10.10.10.245"
output = "ssh on port 22 open and ftp on port 21 open"

for _ in range(3):
    next_command = tool_ollama(f"The last command was:\n{next_command}\nThe output was:\n{output}\nWhat is the next command?")
