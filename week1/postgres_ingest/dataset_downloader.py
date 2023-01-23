import pandas as pd


def load_csv_from(url: str) -> pd.DataFrame:
    return pd.read_csv(url, engine='pyarrow')
