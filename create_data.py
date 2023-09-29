import requests
import json
import random

url = "http://localhost:8000/api/pms/v1/create-data/"

headers = {
    'Content-Type': 'application/json'
}

def create_hum(n):
    n += 1
    if n in range(480, 1000):
        return
    payload = json.dumps({
        "uname": "u1",
        "passw": "p1",
        "sensor_name": "hum",
        "value": random.uniform(15.5, 75.5)
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"hum: {response.text} at {n}")
    create_temp(n)
def create_temp(n):
    n += 1
    payload = json.dumps({
        "uname": "u1",
        "passw": "p1",
        "sensor_name": "temp",
        "value": random.uniform(25.5, 55.5)
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"temp: {response.text} at {n}")
    create_tds(n)
def create_tds(n):
    n += 1
    payload = json.dumps({
        "uname": "u1",
        "passw": "p1",
        "sensor_name": "tds",
        "value": random.uniform(35.5, 75.5)
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"tds: {response.text} at {n}")
    create_hum(n)

if __name__ == "__main__":
    create_hum(0)