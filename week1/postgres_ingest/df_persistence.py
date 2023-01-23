import numpy as np
import pandas as pd
from math import ceil
from typing import List, Tuple


def split_df_in_chunks_with(df: pd.DataFrame, max_chunk_size: int = 100000) -> Tuple[List[pd.DataFrame], int]:
    chunks_qty = ceil(len(df) / max_chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


def persist_df_with(df: pd.DataFrame, conn, table_name: str, if_table_exists='append'):
    df.to_sql(table_name, con=conn, if_exists=if_table_exists, index=False)


def persist_df(df: pd.DataFrame, conn, table_name: str,
               max_chunk_size: int = 100000, if_table_exists='append'):
    chunks, qty = split_df_in_chunks_with(df, max_chunk_size=max_chunk_size)
    for i, chunk in enumerate(chunks):
        # progress.update(task_id=task_id, completed=i+1, total=qty)
        # print(f"Preparing to persist: chunk #{i+1}/{qty}")
        persist_df_with(df=chunk, conn=conn, table_name=table_name, if_table_exists=if_table_exists)
