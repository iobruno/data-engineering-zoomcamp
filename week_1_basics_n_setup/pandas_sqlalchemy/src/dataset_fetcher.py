from typing import List
from collections import namedtuple
import pandas as pd
import math
import numpy as np


class DatasetDownloader:

    Record = namedtuple("Record", ["url", "chunks", "num_chunks"])

    @classmethod
    def fetch_all(cls, endpoints: List[str]) -> List[Record]:
        for endpoint in endpoints:
            yield cls.fetch(endpoint)

    @classmethod
    def fetch(cls, endpoint: str) -> Record:
        df = pd.read_csv(endpoint, engine="pyarrow")
        # Enforces conversion of dataframe cols to lower case, otherwise, in Postgres,
        #  all fields start in uppercase letter will have to be quoted with "" for querying
        df.columns = map(str.lower, df.columns)
        return DatasetDownloader.Record(endpoint, *cls.split_df_in_chunks(df))

    @classmethod
    def split_df_in_chunks(cls, df, chunk_size: int = 100_000) -> (List[pd.DataFrame], int):
        num_chunks = math.ceil(len(df) / chunk_size)
        return np.array_split(df, num_chunks), num_chunks
