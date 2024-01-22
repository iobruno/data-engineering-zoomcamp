from abc import abstractmethod, ABCMeta
from collections import namedtuple
from typing import List
import math
import numpy as np
import pandas as pd
import polars as pl


Record = namedtuple("Record", ["url", "slices"])


class DataframeFetcher(metaclass=ABCMeta):

    def __init__(self, schema=None):
        self.schema = schema

    @abstractmethod
    def fetch(self, endpoint: str) -> Record:
        raise NotImplementedError()

    def fetch_all(self, endpoints: List[str]) -> List[Record]:
        for endpoint in endpoints:
            yield self.fetch(endpoint)

    def with_schema(self, schema):
        self.schema = schema
        return self

    @abstractmethod
    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> List[pd.DataFrame]:
        raise NotImplementedError()


class PolarsFetcher(DataframeFetcher):
    def fetch(self, endpoint: str) -> Record:
        df = pl.read_csv(endpoint, dtypes=self.schema)
        return Record(endpoint, self.slice_df_in_chunks(df))

    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> List[pl.DataFrame]:
        num_chunks = math.ceil(len(df) / chunk_size)
        return [
            df.slice(offset=chunk_id * chunk_size, length=chunk_size)
            for chunk_id in range(num_chunks)
        ]


class PandasFetcher(DataframeFetcher):
    def fetch(self, endpoint: str) -> Record:
        df = pd.read_csv(endpoint, engine='pyarrow', dtype=self.schema)
        # Enforces conversion of dataframe cols to lowercase, otherwise, in Postgres,
        #  all fields starting with an uppercase letter would have to be "quoted" for querying
        df.columns = map(str.lower, df.columns)
        return Record(endpoint, self.slice_df_in_chunks(df))

    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> List[pd.DataFrame]:
        num_chunks = math.ceil(len(df) / chunk_size)
        return np.array_split(df, num_chunks)
