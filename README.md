# ollama-tools
Ollama tools module

## Ollama Tools

Welcome to the `ollama-tools` repository! This project aims to demonstrate the integration of Ollama with various custom functions, showcasing how tool calling support can enhance the capabilities of large language models (LLMs).

## Overview

Ollama is a powerful framework that enables the deployment and management of large language models such as Llama 3.1. By supporting tool calling, Ollama allows these models to interact with external functions and APIs, significantly extending their functionality. This repository provides sample code and examples of how to set up and use tool calling with Ollama.

## Features

- **Tool Calling Support**: Integrate custom functions with LLMs to perform complex tasks.
- **Dynamic Function Execution**: Bind Python functions to the LLM and call them dynamically based on user inputs.
- **Extensible Framework**: Easily add new functions and tools to enhance the model's capabilities.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.11 or higher
- Ollama framework
- Necessary dependencies (`ollama`, `rich`)

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/meirm/ollama-tools.git
cd ollama-tools
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configuration

Set up your environment and configure the necessary tools. The example below demonstrates how to define and use custom functions with Ollama.

### Example Code

Here's a sample code snippet that shows how to integrate custom functions with Ollama:

```python
import ollama 
import json
import requests
from rich import print
import time
import os
import logging
from ollama_tools import generate_function_description
from sample_functions import do_math, get_current_time, get_current_weather

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tools = [
    generate_function_description(get_current_weather),
    generate_function_description(get_current_time),
    generate_function_description(do_math),
]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
functions = [f["function"]["description"] for f in tools]
print("I am a chatbot able to run some functions.\n", "Functions:\n\t", functions)
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
        messages=[{'role': role, 'content': content} for role, content in messages],
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
```

### Running the Example

To run the example, execute the following command:

```bash
python example.py
```

You can then interact with the chatbot and test the custom functions. Type your queries, and the chatbot will respond by calling the appropriate functions dynamically.

## Contributing

We welcome contributions to enhance the functionality of this project. Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or feedback, please open an issue on GitHub or contact the project maintainers.

---

Thank you for using `ollama-tools`. We hope this repository helps you integrate powerful AI capabilities into your applications!
