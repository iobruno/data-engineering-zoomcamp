from abc import abstractmethod, ABCMeta
from collections import namedtuple
from typing import List
import math
import numpy as np
import pandas as pd


Record = namedtuple("Record", ["url", "chunks", "num_chunks"])


class DataframeFetcher(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, endpoint: str) -> Record:
        raise NotImplementedError()

    def fetch_all(self, endpoints: List[str]) -> List[Record]:
        for endpoint in endpoints:
            yield self.fetch(endpoint)

    @abstractmethod
    def split_df_in_chunks(self, df, chunk_size: int = 100_000) -> (List[pd.DataFrame], int):
        raise NotImplementedError()


class PandasFetcher(DataframeFetcher):
    def fetch(self, endpoint: str) -> Record:
        df = pd.read_csv(endpoint, engine="pyarrow")
        # Enforces conversion of dataframe cols to lowercase, otherwise, in Postgres,
        #  all fields starting with an uppercase letter would have to be "quoted" for querying
        df.columns = map(str.lower, df.columns)
        return Record(endpoint, *self.split_df_in_chunks(df))

    def split_df_in_chunks(self, df, chunk_size: int = 100_000) -> (List[pd.DataFrame], int):
        num_chunks = math.ceil(len(df) / chunk_size)
        return np.array_split(df, num_chunks), num_chunks
