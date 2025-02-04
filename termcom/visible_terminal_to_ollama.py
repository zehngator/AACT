import subprocess
import ollama
import platform
import os

# Step 1: Function to open a new terminal, execute a command, and write output to a file
def open_new_terminal_and_capture_output(command, output_file):
    try:
        system = platform.system()
        full_command = f"{command} > {output_file} 2>&1"

        if system == "Windows":
            # For Windows: Open a new terminal and execute the command
            subprocess.Popen(["start", "cmd", "/k", full_command], shell=True)
        elif system == "Linux":
            # For Linux: Open a new terminal and execute the command
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{full_command}; exec bash"])
        elif system == "Darwin":  # macOS
            # For macOS: Open a new Terminal window and execute the command
            subprocess.Popen([
                "osascript", "-e",
                f'tell application "Terminal" to do script "{full_command}"'
            ])
        else:
            print("Unsupported operating system!")
            return False

        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def extract_code(mess: str)-> list[str,str]:
    start = mess.find("'''")
    codetype = mess[:start].split()[-1]
    code = mess[start+3:]
    end = code.find("'''")
    code = code[:end]
    return [codetype,code]

# Step 2: Function to send data to the Ollama model
def send_to_ollama(model, prompt):
    try:
        # Use the Ollama Python library to interact with the model
        response = ollama.chat(model=model, messages=[
  {
    'role': 'user',
    'content': prompt,
  },])
        return response  # Return the response object
    except Exception as e:
        print(f"Exception occurred while communicating with Ollama: {e}")
        return None

# Main Program
if __name__ == "__main__":
    # Command to be executed in the new terminal
    terminal_command = "echo Hello from the new terminal!"
    output_file = "terminal_output.txt"

    # Remove the output file if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Step 1: Open a new terminal and capture the command's output
    print("Opening a new terminal to execute the command...")
    success = open_new_terminal_and_capture_output(terminal_command, output_file)

    if success:
        print(f"Command executed. Waiting for output in '{output_file}'...")
        print("Please close the new terminal when the command finishes.")

        # Wait until the file is created and contains data
        while not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            pass  # Busy wait for the file to be written

        # Step 2: Read the output from the file
        with open(output_file, "r") as file:
            terminal_output = file.read().strip()

        print(f"\nTerminal Output Captured: {terminal_output}")

        # Step 3: Send the captured output to the Ollama model
        model_name = "dolphin-mistral"  # Replace with the model you want to use
        ollama_response = send_to_ollama(model_name, terminal_output)

        if ollama_response:
            print("\nOllama Response:", ollama_response)
        else:
            print("Failed to get a response from Ollama.")
    else:
        print("Failed to open a new terminal.")
