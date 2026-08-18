import requests

print("Starting API request...")

url = "https://www.bankofcanada.ca/valet/observations/V39079/json"

response = requests.get(url, timeout=20)

print("Request completed")
print("Status Code:", response.status_code)

data = response.json()

print("JSON received successfully")
# print(data)