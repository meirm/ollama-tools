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
# log to stderr
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))

tools=[
        generate_function_description(get_current_weather),
        generate_function_description(get_local_time),
        generate_function_description(do_math),
        generate_function_description(get_current_date),
        generate_function_description(query_duckduckgo),
        ]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
# functions_desc = [ f["function"]["description"] for f in tools ]
# print("I am a chatbot able to do run some functions.\n", "Functions:\n\t",  "\n\t".join(functions_desc))
# print()
functions = {function["function"]["name"]: globals()[function["function"]["name"]] for function in tools }


system_prompt_template = """In this environment you have access to a set of tools you can use to answer the user's question.

{{ FORMATTING INSTRUCTIONS }}

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}

Example when you need to know the weather in a city:
<action>[{"function": {"name": "get_current_weather", "arguments": { "city": "New York" }}}]</<action>

{{ USER SYSTEM PROMPT }}"""
# {{ TOOL CONFIGURATION }}"""

user_system_prompt = "You are a friendly bot, you like to chat about the time and weather, and you can do some basic math. If you don't know how to answer a question, you can ask for help."

formatting_instructions = """If you decide that you need to call one or more tools to answer, you should pass the tool request as a list in the following format:
<action>[{"function": {"name": "function_name", "arguments": { "arg1": "value1", "arg2": "value2" }}}]</<action>  
"""


def system_prompt_from_template(template, formatting_instructions, tools, user_system_prompt):
    tool_definitions_str = json.dumps(tools, indent=4)
    return template.replace("{{ TOOL DEFINITIONS IN JSON SCHEMA }}", tool_definitions_str).replace("{{ USER SYSTEM PROMPT }}", user_system_prompt).replace("{{ FORMATTING INSTRUCTIONS }}", formatting_instructions)


system_prompt = system_prompt_from_template(system_prompt_template, formatting_instructions,tools, user_system_prompt)

logging.debug(system_prompt)

# Initial message
initial_greetings = "Hi there."
messages = [
    ('system', system_prompt),
            ('assistant', initial_greetings),
            ]

def query_model(messages):
    response = ollama.chat(
        model='phi4', #'llama3.2',
        messages=[ {'role': role, 'content': content} for role,content in messages ],
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
    )
    logging.debug(response)
    # If the response is empty, it means the model is asking for more information
    if "<action>" in response['message']['content']:
        tools_calls = response['message']['content'].split("<action>")[1].split("</action>")[0]
        logging.info(tools_calls)
        tool_calls_json = json.loads(tools_calls)
        result = use_tools(tool_calls_json, functions)
        messages.append(("tool", result))
        response = query_model(
            messages=messages
            )
        
    result = response['message']['content']
    print("Assistant: ",result)
    messages.append(("assistant", result))

