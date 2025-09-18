import requests
import json

# api config
FMP_API_KEY = ""  
RAPIDAPI_KEY = ""  

FMP_BASE_URL = "https://financialmodelingprep.com/stable"
RAPIDAPI_URL = "https://politician-trade-tracker1.p.rapidapi.com/get_latest_trades"


# fetch data from fmp
def get_senate_disclosures(page=0, limit=10):
    url = f"{FMP_BASE_URL}/senate-latest"
    params = {"page": page, "limit": limit, "apikey": FMP_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_house_disclosures(page=0, limit=10):
    url = f"{FMP_BASE_URL}/house-latest"
    params = {"page": page, "limit": limit, "apikey": FMP_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


#fetch data from ptt
def get_rapidapi_trades():
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "politician-trade-tracker1.p.rapidapi.com",
    }
    response = requests.get(RAPIDAPI_URL, headers=headers)
    response.raise_for_status()
    return response.json()


# normalizing both response schema
def unify_fmp_record(r, chamber_hint=None):
    return {
        "politician": f"{r.get('firstName', '')} {r.get('lastName', '')}".strip(),
        "chamber": chamber_hint or "Unknown",
        "party": None,
        "state": r.get("district"),
        "symbol": r.get("symbol"),
        "company": r.get("assetDescription"),
        "trade_type": r.get("type"),
        "trade_amount": r.get("amount"),
        "trade_date": r.get("transactionDate"),
        "disclosure_date": r.get("disclosureDate"),
        "source": "FMP",
    }


def unify_rapidapi_record(r):
    return {
        "politician": r.get("name"),
        "chamber": r.get("chamber"),
        "party": r.get("party"),
        "state": r.get("state_abbreviation"),
        "symbol": r.get("ticker"),
        "company": r.get("company"),
        "trade_type": r.get("trade_type"),
        "trade_amount": r.get("trade_amount"),
        "trade_date": r.get("trade_date"),
        "disclosure_date": None,
        "source": "RAPIDAPI",
    }



if __name__ == "__main__":
    try:
        final_data = []

        senate_data = get_senate_disclosures(limit=5)
        house_data = get_house_disclosures(limit=5)

        for rec in senate_data:
            final_data.append(unify_fmp_record(rec, chamber_hint="Senate"))

        for rec in house_data:
            final_data.append(unify_fmp_record(rec, chamber_hint="House"))

        rapid_data = get_rapidapi_trades()
        if isinstance(rapid_data, dict):  
            final_data.append(unify_rapidapi_record(rapid_data))
        elif isinstance(rapid_data, list): 
            for rec in rapid_data:
                final_data.append(unify_rapidapi_record(rec))

        print(json.dumps(final_data, indent=2))

    except requests.exceptions.RequestException as e:
        print("error:", e)
