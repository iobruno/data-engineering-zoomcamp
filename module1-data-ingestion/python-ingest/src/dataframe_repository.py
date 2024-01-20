from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union
import pandas as pd
import polars as pl
import sqlalchemy


class SQLRepository(metaclass=ABCMeta):
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.conn = sqlalchemy.create_engine(conn_string).connect()

    def save(self, df: Union[pd.DataFrame, pl.DataFrame]) -> Optional[int]:
        if isinstance(df, pl.DataFrame):
            return self.save_polars_df(df)
        elif isinstance(df, pd.DataFrame):
            return self.save_pandas_df(df)

        raise RuntimeError("Unsupported Dataframe type."
                           "Supported types are pandas or polars Dataframes only")

    def save_polars_df(self, df: pl.DataFrame, engine="adbc"):
        return df.write_database(
            table_name=self.tbl_name,
            connection=self.conn_string,
            if_table_exists="append",
            engine=engine,
        )

    def save_pandas_df(self, df: pd.DataFrame):
        return df.to_sql(self.tbl_name, con=self.conn, if_exists="append", index=False)

    def save_all(self, chunks: List[pd.DataFrame]):
        for chunk in chunks:
            yield self.save(df=chunk)

    @property
    @abstractmethod
    def tbl_name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def with_config(cls, *db_settings) -> "SQLRepository":
        (db_dialect, db_host, db_port, db_name, db_username, db_password) = db_settings
        if db_dialect == "postgresql":
            conn_prefix = f"postgresql"
            db_port = 5432 if db_port is None else db_port
        elif db_dialect == "mysql":
            conn_prefix = f"mysql+mysqlconnector"
            db_port = 3306 if db_port is None else db_port
        else:
            raise Exception("Unsupported dialect. Supported options are ['postgresql', 'mysql']")

        conn_string: str = (
            f"{conn_prefix}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        return cls.__call__(conn_string=conn_string)


class GreenTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "green_taxi_data"


class YellowTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "yellow_taxi_data"


class FhvTaxiRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "fhv_taxi_data"


class ZoneLookupRepository(SQLRepository):
    @property
    def tbl_name(self) -> str:
        return "zone_lookup"
