import requests
import json

API_KEY = ""  
BASE_URL = "https://openapi.ainvest.com/open/ownership/congress"


def get_congress_trades(ticker="AAPL", page=1, size=10):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "ticker": ticker,
        "page": page,
        "size": size
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    trades = get_congress_trades("TSLA", page=1, size=5)
    if trades:
        print("--------", json.dumps(trades, indent=2))
