import argparse
import pandas as pd
from app.extractor import get_cryptos, get_rate
from app.transformer import transform_data
from app.loader import load

def main():

    parser = argparse.ArgumentParser(description="Binance Crypto Price ETL")
    parser.add_argument("--symbol", "--symbols", nargs="+",  dest="symbols", required=True, action="append", help="Trading pair (e.g. BTCUSDT)") 
    parser.add_argument("--output", default="table", choices=["table", "postgres", "json", "csv"])
    args = parser.parse_args() 


    
    crypto_prices = get_cryptos(args.symbols)
    usd_kes_rate = get_rate()
    
    results = []

    
    for sym, price_usdt in crypto_prices.items():
        transformed = transform_data(sym, price_usdt, usd_kes_rate)
        results.append(transformed)
        


    cryptodf = pd.DataFrame(results)
    load(cryptodf, args.output)

if __name__ == "__main__":
    main()
