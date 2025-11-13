# src/generate_synthetic.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_for_store(base, peak_hour=15, noise=0.2):
    # returns 24-length series for a day
    hours = np.arange(24)
    # gaussian peak
    peak = base * (1 + np.exp(-0.5*((hours-peak_hour)/3)**2)*2)
    peak = peak * (1 + np.random.randn(24)*noise)
    return np.clip(peak.round().astype(int), 0, None)

def generate_days(stores_df, days=14):
    rows=[]
    start = datetime(2025,11,1)  # example start date
    for i, r in stores_df.iterrows():
        base = np.random.randint(20,80)  # baseline footfall
        peak_hour = np.random.choice([12,13,14,15,18,19,20])
        for d in range(days):
            day = start + timedelta(days=d)
            series = generate_for_store(base, peak_hour)
            for h, val in enumerate(series):
                ts = datetime(day.year, day.month, day.day, h)
                rows.append({
                    "store_id": r['store_id'],
                    "timestamp": ts.isoformat(),
                    "footfall": int(val)
                })
    return pd.DataFrame(rows)

if __name__=='__main__':
    stores = pd.read_csv("data/stores.csv")
    df = generate_days(stores, days=28)
    df.to_csv("data/footfall_synthetic.csv", index=False)
    print("Saved data/footfall_synthetic.csv")
