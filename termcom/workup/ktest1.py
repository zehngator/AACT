import subprocess, shlex

# Run 'ls' in a separate terminal and capture the output
cmdl = input()
args = shlex.split(cmdl)
print(args)
process = subprocess.Popen(args)
output, error = process.communicate()

print(output.decode('utf-8'))
