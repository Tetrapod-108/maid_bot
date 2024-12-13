import requests
import datetime
import json

def get_weather():
    print("a")

def test():
    with open("test.json") as f:
        data = json.load(f)
        print(data)
        print(data[0]["id"])

test()