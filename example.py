import ollama 
import json
import requests
from rich import print
import time
import os
import logging

from sample_functions import do_math, get_current_time, get_current_weather
from ollama_tools import  generate_function_description, use_tools

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tools=[
        generate_function_description(get_current_weather),
        generate_function_description(get_current_time),
        generate_function_description(do_math),
        ]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
functions_desc = [ f["function"]["description"] for f in tools ]
print("I am a chatbot able to do run some functions.", "Functions:\n\t",  "\n\t".join(functions_desc))
print()
functions = {function["function"]["name"]: globals()[function["function"]["name"]] for function in tools }

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
    result = use_tools(tools_calls, functions)
    print(result)
    messages.append(("assistant", result))

