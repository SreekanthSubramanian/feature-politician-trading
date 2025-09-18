#politician trade tracker api
import requests
import json

API_URL = "https://politician-trade-tracker1.p.rapidapi.com/get_latest_trades"
API_KEY = "" 
API_HOST = "politician-trade-tracker1.p.rapidapi.com"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

try:
    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status() 

    trades = response.json()
    print(json.dumps(trades, indent=2))

    for trade in trades[:5]:
        print(f"- {trade.get('politician', 'Unknown')} | "
              f"{trade.get('transaction_type', 'N/A')} | "
              f"{trade.get('stock', 'N/A')} on {trade.get('date', 'N/A')}")

except requests.exceptions.RequestException as e:
    print("error fetching trades:", e)
