from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(data):
    df = pd.DataFrame(data)

    if df.empty:
        return df

    model = IsolationForest(contamination=0.2, random_state=42)

    df['anomaly'] = model.fit_predict(df[['connections']])

    return df