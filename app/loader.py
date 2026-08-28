import os
import sys
from sqlalchemy import create_engine

def _load_table(results: list):

    if len(results) == 1:
        res = results[0]
        print("\n--------------------------------------------------")
        print("BINANCE CRYPTO PRICE")
        print("--------------------------------------------------")
        print(f"Symbol:            {res['symbol']}")
        print(f"Price USDT:        ${res['price_usdt']:,.2f}")
        print(f"USD/KES Rate:      {res['usd_kes_rate']:.2f}")
        print(f"Approx. Price KES: KSh {res['price_kes']:,.2f}")
        print("--------------------------------------------------")
        print("Source: Binance")
        print("Status: SUCCESS")
        print("--------------------------------------------------")

    else:

        print("\n---------------------------------------------------------------")
        print(f"{'SYMBOL':<14}{'USDT PRICE':<23}{'APPROXIMATE KES'}")
        print("---------------------------------------------------------------")

        for res in results:

            usdt_str = f"${res['price_usdt']:,.2f}"
            kes_str = f"KSh {res['price_kes']:,.2f}"


            print(f"{res['symbol']:<14}{usdt_str:<23}{kes_str}")
        print("---------------------------------------------------------------")



def load (cryptodf, output_format):

    if output_format == "json":
        print(cryptodf.to_json(orient="records", indent=4))

    elif output_format == "csv":
        os.makedirs("data", exist_ok=True)

        cryptodf.to_csv("data/crypto_prices.csv", index=False)
        
        print(cryptodf.to_csv(index=False))

    elif output_format == "postgres":
        
        host = os.getenv("POSTGRES_HOST", "db")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "crypto")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD")
        
        if not password:
            print("ERROR: POSTGRES_PASSWORD environment variable is required.", file=sys.stderr)
            sys.exit(1)
            
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        cryptodf.to_sql("crypto_prices", engine, if_exists="append", index=False)
        print("[LOAD] Data successfully saved to PostgreSQL database.")

    else: 
        results = cryptodf.to_dict(orient="records")
        _load_table(results)
