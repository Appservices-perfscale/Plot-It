from datetime import datetime
import pandas as pd


def convert_to_datetime(date_string, date_format):
    return datetime.strptime(date_string, date_format)

def convert_to_timestamp_series(series):
    try:
        return pd.to_datetime(series, unit='s')
    except Exception:
        return pd.to_datetime(series)
