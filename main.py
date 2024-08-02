import ollama 
import inspect
import json
import requests
from rich import print
import time

def generate_function_description(func):
    func_name = func.__name__
    docstring = func.__doc__

    # Get function signature
    sig = inspect.signature(func)
    params = sig.parameters

    # Create the properties for parameters
    properties = {}
    required = []

    for param_name, param in params.items():
        param_type = 'string'  # Default type; adjust as needed based on annotations
        if param.annotation != inspect.Parameter.empty:
            param_type = param.annotation.__name__.lower()

        properties[param_name] = {
            'type': param_type,
            'description': f'The name of the {param_name}',
        }
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    # Create the JSON object
    function_description = {
            'type': 'function',
            'function': {
                'name': func_name,
                'description': docstring,
                'parameters': {
                    'type': 'object',
                    'properties': properties,
                    'required': required,
                },
            },
    }

    return function_description
    # Return JSON formatted string
    return json.dumps(function_description, indent=2)

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
        ]
print("Tools:")
print(json.dumps(tools, indent=4))

response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 
               # 'content': 'What is the weather in Toronto?',
               'content': 'What is the time?',
               }
              ],

    tools=tools,
)

tools_calls = response['message']['tool_calls']
print(tools_calls)
# Parse tool name and arguments
tool_name = tools_calls[0]['function']['name']
arguments = tools_calls[0]['function']['arguments']

if tool_name == "get_current_weather":
    city = arguments['city']

    # Call the function with parsed arguments
    result = get_current_weather(city)
elif tool_name == "get_current_time":
    result = get_current_time()
    
print(result)
