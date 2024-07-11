import requests
import json

url = "http://127.0.0.1:5000/ask"
headers = {"Content-Type": "application/json"}
data = {
    "question": "What is the capital of France?"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Failed to get a response. Status code:", response.status_code)
