import ollama 
import requests
from rich import print

def get_current_weather(city):
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"

response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 
        'What is the weather in Toronto?'}],

    tools=[{
      'type': 'function',
      'function': {
        'name': 'get_current_weather',
        'description': 'Get the current weather for a city',
        'parameters': {
          'type': 'object',
          'properties': {
            'city': {
              'type': 'string',
              'description': 'The name of the city',
            },
          },
          'required': ['city'],
        },
      },
    },
  ],
)

tools_calls = response['message']['tool_calls']

# Parse tool name and arguments
tool_name = tools_calls[0]['function']['name']
arguments = tools_calls[0]['function']['arguments']
city = arguments['city']

# Call the function with parsed arguments
result = get_current_weather(city)
print(result)
