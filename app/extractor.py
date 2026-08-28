import sys
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_cryptos(symbols_raw):
    base_url = os.getenv("Binance", "https://api.binance.com/api/v3/ticker/price")

    # If symbols_raw is passed directly as a string, wrap it in a list
    if isinstance(symbols_raw, str):
        symbols_raw = [symbols_raw]

    cleaned_symbols = []
    
    # Flatten nested structures and split comma-separated strings
    def extract_symbols(raw):
        if isinstance(raw, str):
            for part in raw.split(","):
                token = part.strip().upper()
                if token and token not in cleaned_symbols:
                    cleaned_symbols.append(token)
        elif isinstance(raw, (list, tuple, set)):
            for element in raw:
                extract_symbols(element)

    extract_symbols(symbols_raw)

    if not cleaned_symbols:
        print("ERROR: No valid symbols provided.")
        sys.exit(1)

    try:
        # Single symbol query
        if len(cleaned_symbols) == 1:
            params = {"symbol": cleaned_symbols[0]}
        # Batch symbols query (JSON list format required by Binance)
        else:
            params = {"symbols": json.dumps(cleaned_symbols, separators=(',', ':'))}

        response = requests.get(base_url, params=params, timeout=10)

        if response.status_code == 400:
            print(f"ERROR: One or more symbols in {cleaned_symbols} is invalid.")
            sys.exit(1)

        response.raise_for_status()
        data = response.json()

        # Format into { "SYMBOL": price }
        if isinstance(data, list):
            return {item["symbol"]: float(item["price"]) for item in data}
        return {data["symbol"]: float(data["price"])}

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)




def get_rate():

    xurl = os.getenv("Frankfurter","https://api.frankfurter.dev/v2/rate/USD/KES")
    
    try:
        response = requests.get(xurl, timeout = 10)
        response.raise_for_status()
        
        xdata = response.json()
        return float(xdata["rate"])
        

    except (requests.RequestException, KeyError):
        print("ERROR: Unable to retrieve the USD/KES exchange rate.")
        sys.exit(1)
