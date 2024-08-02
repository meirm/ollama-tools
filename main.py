import ollama 
import json
import requests
from rich import print
import time

from ollama_tools import  generate_function_description

def do_math(a:int, op:str, b:int)->int:
    """Do basic math operations"""
    if op == "+":
        return int(a) + int(b)
    elif op == "-":
        return int(a) - int(b)
    elif op == "*":
        return int(a) * int(b)
    elif op == "/":
        if int(b) == 0: 
            return "Nan"
        else:
            return int(a)/int(b)
    else:
        return "Nan"

def get_current_time():
    """Get the current time"""
    current_time = time.strftime("%H:%M:%S")
    return current_time

def get_current_weather(city):
    """Get the current weather for a city"""
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"


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

