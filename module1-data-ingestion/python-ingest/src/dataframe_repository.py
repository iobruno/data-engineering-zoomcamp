from abc import ABCMeta, abstractmethod
from typing import List, Optional

import pandas as pd
import polars as pl
import sqlalchemy


class SQLRepository(metaclass=ABCMeta):
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.conn = sqlalchemy.create_engine(conn_string).connect()

    def save(self, df: pd.DataFrame | pl.DataFrame, write_disposition: str) -> Optional[int]:
        if isinstance(df, pl.DataFrame):
            return self.save_polars_df(df, write_disposition)
        elif isinstance(df, pd.DataFrame):
            return self.save_pandas_df(df, write_disposition)
        raise RuntimeError(
            "Unsupported Dataframe type." "Supported types are pandas or polars Dataframes only"
        )

    def save_polars_df(self, df: pl.DataFrame, write_disposition: str, engine="adbc"):
        return df.write_database(
            table_name=self.tbl_name,
            connection=self.conn_string,
            if_table_exists=write_disposition,
            engine=engine,
        )

    def save_pandas_df(self, df: pd.DataFrame, write_disposition):
        return df.to_sql(self.tbl_name, con=self.conn, if_exists=write_disposition, index=False)

    def save_all(self, chunks: List[pd.DataFrame]):
        for chunk in chunks:
            yield self.save(df=chunk, write_disposition="append")

    @property
    @abstractmethod
    def tbl_name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def with_config(cls, *db_settings) -> "SQLRepository":
        (db_host, db_port, db_name, db_username, db_password) = db_settings
        db_port = 5432 if db_port is None else db_port
        conn_string = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        return cls.__call__(conn_string=conn_string)


class GreenTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "green_taxi_trips"


class YellowTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "yellow_taxi_trips"


class FhvTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "fhv_trips"


class ZoneLookupRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "zone_lookup"
