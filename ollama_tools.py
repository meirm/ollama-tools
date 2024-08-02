import inspect
import json

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
