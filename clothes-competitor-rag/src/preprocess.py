# src/preprocess.py
import pandas as pd
def preprocess():
    stores = pd.read_csv("data/stores.csv")
    foot = pd.read_csv("data/footfall_synthetic.csv", parse_dates=['timestamp'])
    foot['hour'] = foot['timestamp'].dt.hour
    agg = foot.groupby(['store_id','hour']).footfall.sum().reset_index()
    # compute peak hour per store
    peak = agg.loc[agg.groupby('store_id').footfall.idxmax()][['store_id','hour','footfall']]
    peak = peak.rename(columns={'hour':'peak_hour','footfall':'peak_count'})
    peak.to_csv("data/store_peak_hours.csv", index=False)
    # Also save hourly aggregates per store
    agg.to_csv("data/footfall_hourly_agg.csv", index=False)
    print("Saved aggregates")
if __name__=='__main__':
    preprocess()
