import inspect
import json
import re
def generate_function_description(func):
    func_name = func.__name__
    docstring = func.__doc__

    # Get function signature
    sig = inspect.signature(func)
    params = sig.parameters

    # Create the properties for parameters
    properties = {}
    required = []

    # Process the docstring to extract argument descriptions
    arg_descriptions = {}
    if docstring:
        # remove leading/trailing whitespace or leading empty lines and split into lines
        docstring = re.sub(r'^\s*|\s*$', '', docstring, flags=re.MULTILINE)
        lines = docstring.split('\n')
        current_arg = None
        for line in lines:
            line = line.strip()
            if line:
                if ':' in line:
                    # strip leading/trailing whitespace and split into two parts
                    line = re.sub(r'^\s*|\s*$', '', line)
                    parts = line.split(':', 1)
                    if parts[0] in params:
                        current_arg = parts[0]
                        arg_descriptions[current_arg] = parts[1].strip()
                elif current_arg:
                    arg_descriptions[current_arg] += ' ' + line.strip()

    for param_name, param in params.items():
        param_type = 'string'  # Default type; adjust as needed based on annotations
        if param.annotation != inspect.Parameter.empty:
            param_type = param.annotation.__name__.lower()

        param_description = arg_descriptions.get(param_name, f'The name of the {param_name}')

        properties[param_name] = {
            'type': param_type,
            'description': param_description,
        }
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    # Create the JSON object
    function_description = {
        'type': 'function',
        'function': {
            'name': func_name,
            'description': docstring.split('\n')[0] if docstring else f'Function {func_name}',
            'parameters': {
                'type': 'object',
                'properties': properties,
                'required': required,
            },
        },
    }

    return function_description


def use_tools(tools_calls, tool_functions):
    tools_responses = []
    for tool_call in tools_calls:
        # Parse tool name and arguments
        tool_name = tool_call['function']['name']
        arguments = tool_call['function']['arguments']

        # Dynamically call the function
        if tool_name in tool_functions:
            result = tool_functions[tool_name](**arguments)
            tools_responses.append(str(result))
        else:
            raise KeyError(f"Function {tool_name} not found in the provided tool functions.")
    return "\n".join(tools_responses)
