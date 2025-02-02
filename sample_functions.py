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
    Do basic math operations.

    Args:
        a: The first number.
        op: The operation to perform (+, -, *, /).
        b: The second number.

    Returns:
        The result of the operation as a string.
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

def get_current_date(date_format="%Y-%m-%d") -> str:
    """Get the current date.

    Args:
        date_format: The format to return the date in. Default is %Y-%m-%d.
    
    Returns:
        A string with the current date in the requested format.
    """
    current_date = time.strftime(date_format)
    return f"{current_date}"

def get_local_time() -> str:
    """Get the current local time.
    
    Returns:
        A string with the current time in HH:MM:SS format.
    """
    current_time = time.strftime("%H:%M:%S")
    return f"{current_time}"

def get_current_weather(city:str) -> str:
    """Get the current weather for a city.

    Args:
        city: The city to get the weather for.

    Returns:
        A string with the current temperature in Celsius for the city.
    """
    base_url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"


