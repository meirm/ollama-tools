import ollama 
import json
import requests
from rich import print
import time

from ollama_tools import  generate_function_description

from sample_functions import do_math, get_current_time, get_current_weather

tools=[
        generate_function_description(get_current_weather),
        generate_function_description(get_current_time),
        generate_function_description(do_math),
        ]

print("Tools:")
print(json.dumps(tools, indent=4))

response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 
               'content': 'How much is 99 * 180',
               #'content': 'How much is 99 - 180',
               #'content': 'How much is 99 + 180',
               #'content': 'What is the weather in Toronto?',
               # 'content': 'What is the time?',
               }
              ],

    tools=tools,
)


tools_calls = response['message']['tool_calls']
print(tools_calls)
# Parse tool name and arguments
tool_name = tools_calls[0]['function']['name']
arguments = tools_calls[0]['function']['arguments']

# Dynamically call the function
result = globals()[tool_name](**arguments)

print(result)

