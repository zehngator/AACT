import openai

def chat_with_gpt(prompts, api_key):
    responses = []
    
    # Define the function (tool) for command-line responses
    function_definitions = [
        {
            "name": "get_command",
# module, of which there are so many ways to do so            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "A command-line command to achieve the given task."
                    }
                },
                "required": ["command"]
            }
        ]

    for prompt in prompts:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",  # Use "gpt-4" or "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": "You are an AI that always provides command-line commands."},
                    {"role": "user", "content": prompt}
                ],
                functions=function_definitions,
                function_call={"name": "get_command"}  # Forces ChatGPT to use the function
            )

            cmd_response = response["choices"][0]["message"]["function_call"]["arguments"]
            responses.append(cmd_response)
        except Exception as e:
            responses.append(f"Error: {e}")

    return responses

if __name__ == "__main__":
    api_key = "your-api-key-here"  # Replace with your OpenAI API key
    openai.api_key = api_key

    prompts = [
        "How do I list all files in a directory?",
        "How do I find a process by name in Linux?",
        "How do I check disk usage in Windows?"
    ]

    responses = chat_with_gpt(prompts, api_key)
    
    for i, response in enumerate(responses):
        print(f"Prompt: {prompts[i]}\nCommand: {response}\n")
