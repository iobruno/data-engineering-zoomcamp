from math import ceil
from typing import List, Tuple

import numpy as np
import pandas as pd


def split_df_in_chunks_with(df: pd.DataFrame,
                            max_chunk_size: int = 100000) -> Tuple[List[pd.DataFrame], int]:
    chunks_qty = ceil(len(df) / max_chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


def persist_df_with(df: pd.DataFrame, conn, table_name: str, if_table_exists='append'):
    df.to_sql(table_name, con=conn, if_exists=if_table_exists, index=False)
