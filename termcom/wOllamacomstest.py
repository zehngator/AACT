import subprocess
import ollama

response = ollama.chat(model='dolphin-mistral', messages=[
  {
    'role': 'user',
    'content': 'Make guitar tabs for something in the orange',
  },
])

print(response['message']['content'])
