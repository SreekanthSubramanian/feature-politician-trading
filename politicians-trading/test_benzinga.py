# benzinga api
import requests
import json

api_key = ""

url = "https://api.benzinga.com/api/v1/gov/usa/congress/trades"

params = {
    "token": api_key,
    "pagesize": 10,        
    # "chamber": "House",     
    "date_from": "2025-09-01",
    "date_to": "2025-09-16"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    trades = response.json()
    print("------", json.dumps(trades, indent=2))
else:
    print("error:", response.status_code, response.text)
