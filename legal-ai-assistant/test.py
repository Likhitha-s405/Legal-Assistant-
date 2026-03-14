

import requests

url = "https://unhealed-unosmotic-tova.ngrok-free.dev/generate"

data = {
    "prompt": "Explain fundamental rights in India",
    "max_new_tokens": 100
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Raw Text:", response.text)
print("JSON:", response.json())