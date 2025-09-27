# stock_data.py
import requests
import pandas as pd
import os
from datetime import datetime
FINNHUB_TOKEN = "d3bo2l9r01qqg7bvdvigd3bo2l9r01qqg7bvdvj0"

def batch_fetch(symbols: list[str]) -> pd.DataFrame:
    rows = []
    for sym in symbols:
        url = f"https://finnhub.io/api/v1/quote?symbol={sym}&token={FINNHUB_TOKEN}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        rows.append({
            "symbol": sym,
            "price": float(data["c"]),
            "prev_close": data["pc"],
            "pct_change": ((data["c"] - data["pc"]) / data["pc"] * 100) if data["pc"] else 0.0,
            "timestamp": datetime.utcnow().isoformat(),
        })

    return pd.DataFrame(rows)
