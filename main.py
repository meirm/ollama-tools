import ollama 
import json
import requests
from rich import print
import time
import os
import logging
from ollama_tools import  generate_function_description

from sample_functions import do_math, get_current_time, get_current_weather

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tools=[
        generate_function_description(get_current_weather),
        generate_function_description(get_current_time),
        generate_function_description(do_math),
        ]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
functions = [ f["function"]["description"] for f in tools ]
print("I am a chatbot able to do run some functions.\n", "Functions:\n\t",  functions)
messages = []
while True:
    query = input()
    if query == "quit":
        break
    if query.strip() == "":
        continue
    messages.append(("user", query))
    response = ollama.chat(
        model='llama3.1',
        messages=[ {'role': role, 'content': content} for role,content in messages ],
        tools=tools,
    )

    tools_calls = response['message']['tool_calls']
    logging.debug(tools_calls)
    # Parse tool name and arguments
    tool_name = tools_calls[0]['function']['name']
    arguments = tools_calls[0]['function']['arguments']

    # Dynamically call the function
    result = globals()[tool_name](**arguments)
    print(result)
    messages.append(("assistant", result))

