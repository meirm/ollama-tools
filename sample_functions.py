import json
import requests
import time

def do_math(a:int, op:str, b:int)->int:
    """Do basic math operations"""
    if op == "+":
        return int(a) + int(b)
    elif op == "-":
        return int(a) - int(b)
    elif op == "*":
        return int(a) * int(b)
    elif op == "/":
        if int(b) == 0: 
            return "Nan"
        else:
            return int(a)/int(b)
    else:
        return "Nan"

def get_current_time() -> str:
    """Get the current time"""
    current_time = time.strftime("%H:%M:%S")
    return f"The current time is {current_time}"

def get_current_weather(city:str) -> str:
    """Get the current weather for a city"""
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    data = response.json()
    return f"The current temperature in {city} is: {data['current_condition'][0]['temp_C']}°C"


