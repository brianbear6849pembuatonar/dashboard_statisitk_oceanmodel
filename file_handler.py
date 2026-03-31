import pandas as pd

def load_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

def auto_detect_time_column(df):
    for col in df.columns:
        if 'time' in col.lower() or 'date' in col.lower() or 'timestamp' in col.lower():
            return col
    return None