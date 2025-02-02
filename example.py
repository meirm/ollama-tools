import ollama 
import json
import requests
from rich import print
import time
import os
import logging
import sys
import argparse

from sample_functions import do_math, get_local_time, get_current_weather, query_duckduckgo
from sample_functions import get_current_date
from ollama_tools import  generate_function_description, use_tools

parser = argparse.ArgumentParser(description='Chatbot example')
parser.add_argument('--logging', type=str, default='INFO', help='Logging level')
args = parser.parse_args()

# Configure logging
logging.basicConfig(level=args.logging, format='%(asctime)s - %(levelname)s - %(message)s')

tools=[
        generate_function_description(get_current_weather),
        generate_function_description(get_local_time),
        generate_function_description(do_math),
        generate_function_description(get_current_date),
        generate_function_description(query_duckduckgo),
        ]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
functions_desc = [ f["function"]["description"] for f in tools ]
print("I am a chatbot able to do run some functions.\n", "Functions:\n\t",  "\n\t".join(functions_desc))
print()
functions = {function["function"]["name"]: globals()[function["function"]["name"]] for function in tools }

# Initial message
initial_greetings = "Hi, I'm a chatbot. You can ask me questions or ask me to do things. I may ask you for more information if needed and if I can't answer your question, I'll let you know."
messages = [
            # ('assistant', initial_greetings),
            ]

def query_model(messages, tools):
    response = ollama.chat(
        model='llama3.2',
        messages=[ {'role': role, 'content': content} for role,content in messages ],
        tools=tools,
    )
    return response

print("Assistant: ", initial_greetings)
print("You can type 'quit' to exit the chatbot.")
# print("Assistant: ", initial_greetings)
while True:
    try:
        query = input("User: ")
    except EOFError:
        break
    if query == "quit":
        break
    if query.strip() == "":
        continue
    messages.append(("user", query))
    response = query_model(
        messages=messages,
        tools=tools,
    )
    # If the response is empty, it means the model is asking for more information
    if response['message']['content'] == "":
        tools_calls = response['message']['tool_calls']
        # logging.debug(tools_calls)
        result = use_tools(tools_calls, functions)
        messages.append(("tool", result))
        response = query_model(
            messages=messages,
            tools=tools,
            )
        
    result = response['message']['content']
    print("Assistant: ",result)
    messages.append(("assistant", result))

