import subprocess
import platform
import ollama
import threading
import time

# Step 1: Function to open a persistent terminal
def open_persistent_terminal():
    system = platform.system()

    try:
        if system == "Windows":
            # Open a persistent CMD terminal
            terminal = subprocess.Popen(
                ["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        elif system == "Linux":
            # Open a persistent Bash terminal
            terminal = subprocess.Popen(
                ["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        elif system == "Darwin":  # macOS
            # Open a persistent Bash terminal
            terminal = subprocess.Popen(
                ["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        else:
            print("Unsupported operating system!")
            return None

        return terminal
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# Step 2: Function to send a command to the terminal
def send_command_to_terminal(terminal, command):
    try:
        if terminal:
            # Write the command to the terminal
            terminal.stdin.write(command + "\n")
            terminal.stdin.flush()
    except Exception as e:
        print(f"Error sending command to terminal: {e}")

# Step 3: Function to continuously read terminal output
def read_terminal_output(terminal):
    try:
        if terminal:
            while True:
                output = terminal.stdout.readline()
                if output:
                    print(output.strip())  # Display the terminal's output in real time
    except Exception as e:
        print(f"Error reading from terminal: {e}")

# Step 4: Function to send data to Ollama
def send_to_ollama(model, prompt):
    try:
        response = ollama.chat(model=model, prompt=prompt)
        return response
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return None

# Main Program
if __name__ == "__main__":
    # Open a persistent terminal
    print("Opening a persistent terminal...")
    terminal = open_persistent_terminal()

    if terminal:
        # Start a thread to read the terminal output
        threading.Thread(target=read_terminal_output, args=(terminal,), daemon=True).start()

        print("Terminal is ready. Type commands to send to the terminal.")
        print("Type 'exit' to close the terminal.")

        # Main loop to interact with the terminal and Ollama
        while True:
            # Get a command from the user
            user_input = input("Command to terminal: ")
            
            if user_input.lower() == "exit":
                # Close the terminal session
                terminal.stdin.write("exit\n")
                terminal.stdin.flush()
                time.sleep(1)
                terminal.terminate()
                print("Terminal closed.")
                break

            # Send the command to the terminal
            send_command_to_terminal(terminal, user_input)

            # Send the command to Ollama
            ollama_response = send_to_ollama("llama-2", user_input)
            if ollama_response:
                print("Ollama Response:", ollama_response)

