import json
import requests
import time

def query_duckduckgo(query: str) -> str:
    """
    Query the DuckDuckGo Instant Answer API and return the results.
    query: The search query to send to DuckDuckGo.
    Returns:
        A summary of the top result from DuckDuckGo.
    """
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extracting the abstract or top result
        result = data.get('AbstractText')
        if not result:
            related_topics = data.get('RelatedTopics', [])
            if related_topics:
                result = related_topics[0].get('Text', 'No result found.')
            else:
                result = 'No result found.'
        #print(result)
        return result
    else:
        return "Error querying DuckDuckGo API."

# Example function with description
def get_duckduckgo_result(query: str) -> str:
    """
    Get the top DuckDuckGo search result for the given query.
    query: The search query to send to DuckDuckGo.
    """
    return query_duckduckgo(query)


def do_math(a:int, op:str, b:int)->str:
    """
    Do basic math operations
    a: The first operand
    op: The operation to perform (one of '+', '-', '*', '/')
    b: The second operand
    """
    res = "Nan"
    if op == "+":
        res = str(int(a) + int(b))
    elif op == "-":
        res = str(int(a) - int(b))
    elif op == "*":
        res = str(int(a) * int(b))
    elif op == "/":
        if int(b) != 0:
            res = str(int(a) / int(b))
    return res

def get_current_time() -> str:
    """Get the current time"""
    current_time = time.strftime("%H:%M:%S")
    return f"The current time is {current_time}"

def get_current_weather(city:str) -> str:
    """Get the current weather for a city
    Args:
        city: The city to get the weather for
    """
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"


