#financialmodeling prep api
import requests
import json

API_KEY = ""   

BASE_URL = "https://financialmodelingprep.com/stable"

def get_senate(page=0, limit=10):
    url = f"{BASE_URL}/senate-latest"
    params = {
        "page": page,
        "limit": limit,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_house(page=0, limit=10):
    url = f"{BASE_URL}/house-latest"
    params = {
        "page": page,
        "limit": limit,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        senate_data = get_senate(limit=1)
        house_data = get_house(limit=1)

        print("---- Senate ----")
        print(json.dumps(senate_data, indent=2))

        print("---- House ----")
        print(json.dumps(house_data, indent=2))

    except requests.exceptions.RequestException as e:
        print("API call failed:", e)
