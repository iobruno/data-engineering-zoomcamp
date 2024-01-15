from abc import abstractmethod
from typing import List, Optional
import pandas as pd
import sqlalchemy


class SQLRepository:
    def __init__(self, conn_string: str, table_name: str):
        self.conn_string = conn_string
        self.conn = sqlalchemy.create_engine(conn_string).connect()
        self.table_name = table_name

    @abstractmethod
    def save(self, df: pd.DataFrame, if_exists="append") -> Optional[int]:
        raise NotImplementedError

    def save_all(self, chunks: List[pd.DataFrame], if_exists="append"):
        for chunk in chunks:
            yield self.save(df=chunk, if_exists=if_exists)

    @classmethod
    def with_config(cls, tbl_name: str, *db_settings):
        (db_dialect, db_host, db_port, db_name, db_username, db_password) = db_settings
        if db_dialect == "postgres":
            conn_prefix = f"postgresql+psycopg"
            db_port = 5432 if db_port is None else db_port
        elif db_dialect == "mysql":
            conn_prefix = f"mysql+mysqlconnector"
            db_port = 3306 if db_port is None else db_port
        else:
            raise Exception("Unsupported database dialect. Supported options are 'mysql' or 'postgres'")

        conn_string: str = f'{conn_prefix}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
        return GreenTaxiRepository(conn_string, tbl_name)


class GreenTaxiRepository(SQLRepository):
    def save(self, df, if_exists="append") -> Optional[int]:
        return df.to_sql(self.table_name, con=self.conn, if_exists="append", index=False)


class YellowTaxiRepository(SQLRepository):

    def save(self, df, if_exists="append") -> Optional[int]:
        return df.to_sql(self.table_name, conn=self.conn, if_exists=if_exists, index=False)


class FhvTaxiRepository(SQLRepository):
    def save(self, df, if_exists="append") -> Optional[int]:
        return df.to_sql(self.table_name, conn=self.conn, if_exists=if_exists, index=False)


class ZoneLookupRepository(SQLRepository):
    def save(self, df, if_exists="append") -> Optional[int]:
        return df.to_sql(self.table_name, conn=self.conn, if_exists=if_exists, index=False)
