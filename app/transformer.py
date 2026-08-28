def transform_data(symbol: str, price_usdt: float, usd_kes_rate: float) -> dict:

    price_kes = float(price_usdt) * float(usd_kes_rate)

    return {
        "symbol": symbol,
        "price_usdt": round(price_usdt, 2),
        "usd_kes_rate": round(usd_kes_rate, 2),
        "price_kes": round(price_kes, 2)
    }
