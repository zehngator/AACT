import subprocess
import ollama
import platform

#created mostly by Chatgpt
#allows for successful communication between the terminal and ollama
#allos me to query the command line and give the results to ollama but does not open a terminal so I can see it
#
# Step 1: Function to execute code in another terminal and capture output
def execute_code_in_terminal(command):
    try:
        # Open a subprocess and stream the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = ""

        # Read and print output line-by-line
        for line in process.stdout:
            print(line, end="")  # Print to console in real-time
            output += line  # Append to the captured output

        # Wait for the process to finish and capture return code
        process.wait()
        
        # Check if the command succeeded
        if process.returncode == 0:
            return output.strip()  # Return the captured output
        else:
            print(f"Error: {process.stderr.read()}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


# Step 2: Function to send data to the Ollama model
def send_to_ollama(model, prompt):
    print(f"heres the prompt {prompt}")
    try:
        # Use the Ollama Python library to interact with the model
        response = ollama.chat(model=model, messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])
        return response  # Return the response object
    except Exception as e:
        print(f"Exception occurred while communicating with Ollama: {e}")
        return None

# Main Program
if __name__ == "__main__":
    # Command to be executed in the terminal (modify as needed)
    terminal_command = "echo can you help me solve a ctf at ip: 123.54.90.200 and only give me the one cmdline argument i need!"

    # Step 1: Execute the command in another terminal and get the output
    result = execute_code_in_terminal(terminal_command)

    if result:
        print(f"Terminal Output: {result}")

        # Step 2: Send the output to the Ollama model
        model_name = "dolphin-mistral"  # Replace with the model you want to use
        ollama_response = send_to_ollama(model_name, result)

        if ollama_response:
            print("Ollama Response:", ollama_response['message']['content'])
        else:
            print("Failed to get a response from Ollama.")
    else:
        print("Failed to execute the terminal command.")

