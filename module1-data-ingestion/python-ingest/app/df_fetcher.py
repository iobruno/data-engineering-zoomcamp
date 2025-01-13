from abc import ABCMeta, abstractmethod
from collections import namedtuple

import pandas as pd
import polars as pl

Record = namedtuple("Record", ["url", "slices"])


class DataframeFetcher(metaclass=ABCMeta):
    schema: str = None
    renaming_strategy: dict = {}

    def fetch_all(self, endpoints: list[str]) -> list[Record]:
        for endpoint in endpoints:
            yield self.fetch(endpoint)

    def with_schema(self, schema) -> "DataframeFetcher":
        self.schema = schema
        return self

    def with_renaming_strategy(self, renaming) -> "DataframeFetcher":
        self.renaming_strategy = renaming
        return self

    @abstractmethod
    def fetch(self, endpoint: str) -> Record:
        raise NotImplementedError()

    @abstractmethod
    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> list[pd.DataFrame]:
        raise NotImplementedError()


class PolarsFetcher(DataframeFetcher):
    def fetch(self, endpoint: str) -> Record:
        df = pl.read_csv(endpoint, schema_overrides=self.schema)
        df = df.rename(self.renaming_strategy)
        return Record(endpoint, self.slice_df_in_chunks(df))

    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> list[pl.DataFrame]:
        return [
            df.slice(offset=chunk_id, length=chunk_size)
            for chunk_id in range(0, len(df), chunk_size)
        ]


class PandasFetcher(DataframeFetcher):
    def fetch(self, endpoint: str) -> Record:
        df = pd.read_csv(endpoint, engine="pyarrow", dtype=self.schema)
        df = df.rename(columns=self.renaming_strategy)
        return Record(endpoint, self.slice_df_in_chunks(df))

    def slice_df_in_chunks(self, df, chunk_size: int = 100_000) -> list[pd.DataFrame]:
        return [
            df.iloc[chunk_id : chunk_id + chunk_size]
            for chunk_id in range(0, len(df), chunk_size)
        ]
