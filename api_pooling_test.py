import requests

url = "http://gh.localhost:9090/tenants/login/"

payload = {
    "email": "gh@gmail.com",
    "password": "gh"
}

headers = {
    "Content-Type": "application/json"
}

for i in range(50):   # send 50 requests
    response = requests.post(url, json=payload, headers=headers)
    print(f"Request {i+1} -> Status:", response.status_code)
    print("Response:", response.text)