from abc import ABCMeta, abstractmethod
from typing import List, Optional
import pandas as pd
import sqlalchemy


class SQLRepository(metaclass=ABCMeta):
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.conn = sqlalchemy.create_engine(conn_string).connect()

    def save(self, df: pd.DataFrame) -> Optional[int]:
        return df.to_sql(self.tbl_name, con=self.conn, if_exists="append", index=False)

    def save_all(self, chunks: List[pd.DataFrame]):
        for chunk in chunks:
            yield self.save(df=chunk)

    @property
    @abstractmethod
    def tbl_name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def with_config(cls, *db_settings) -> 'SQLRepository':
        (db_dialect, db_host, db_port, db_name, db_username, db_password) = db_settings
        if db_dialect == "postgresql":
            conn_prefix = f"postgresql+psycopg"
            db_port = 5432 if db_port is None else db_port
        elif db_dialect == "mysql":
            conn_prefix = f"mysql+mysqlconnector"
            db_port = 3306 if db_port is None else db_port
        else:
            raise Exception("Unsupported database dialect. Supported options are 'mysql' or 'postgres'")

        conn_string: str = f'{conn_prefix}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
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
