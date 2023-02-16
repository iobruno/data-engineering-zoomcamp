from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect import flow, task
from prefect_gcp import GcsBucket

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
schema_file = root_dir.joinpath("schemas.yml")

cfg = OmegaConf.load(config_file)
schemas = OmegaConf.load(schema_file)


class DataFrameSerializationFormat(Enum):
    """An enumeration class to represent different file formats,
        compression options for upload_from_dataframe

    Attributes:
        CSV: Representation for 'csv' file format with no compression
            and its related content type and suffix.

        CSV_GZIP: Representation for 'csv' file format with 'gzip' compression
            and its related content type and suffix.

        PARQUET: Representation for 'parquet' file format with no compression
            and its related content type and suffix.

        PARQUET_SNAPPY: Representation for 'parquet' file format
            with 'snappy' compression and its related content type and suffix.

        PARQUET_GZIP: Representation for 'parquet' file format
            with 'gzip' compression and its related content type and suffix.
    """

    CSV = ('csv', None, 'text/csv', '.csv')
    CSV_GZIP = ('csv', 'gzip', 'application/x-gzip', '.csv.gz')
    PARQUET = ('parquet', None, 'application/octet-stream', '.parquet')
    PARQUET_SNAPPY = ('parquet', 'snappy', 'application/octet-stream', '.parquet.snappy')
    PARQUET_GZIP = ('parquet', 'gzip', 'application/octet-stream', '.parquet.gz')

    @property
    def format(self):
        return self.value[0]

    @property
    def compression(self):
        return self.value[1]

    @property
    def content_type(self):
        return self.value[2]

    @property
    def suffix(self):
        return self.value[3]

    def fix_extension_with(self, gcs_blob_path: str) -> str:
        """Fix the extension of a GCS blob.

        Args:
            gcs_blob_path: The path to the GCS blob to be modified.

        Returns:
            The modified path to the GCS blob with the new extension.
        """
        gcs_blob_path = Path(gcs_blob_path)
        folder = gcs_blob_path.parent
        filename = Path(gcs_blob_path.stem).with_suffix(self.suffix)
        return str(folder.joinpath(filename).as_posix())


@task(log_prints=True)
def upload_from_dataframe(
        prefect_gcs_block: str,
        df: pd.DataFrame,
        to_path: str,
        serialization_format: Union[str, DataFrameSerializationFormat] = 'parquet_snappy',
        **upload_kwargs: Dict[str, Any]):
    """Upload a Pandas DataFrame to Google Cloud Storage in various formats.

    This function uploads the data in a Pandas DataFrame to Google Cloud Storage
    in a specified format, such as .csv, .csv.gz, .parquet, .parquet.snappy, and .parquet.gz.

    Args:
        prefect_gcs_block: The Prefect GcsBlock name
        df: The Pandas DataFrame to be uploaded.
        to_path: The destination path for the uploaded DataFrame.
        serialization_format: The format to serialize the DataFrame into.
            When passed as a `str`, the valid options are:
            'csv', 'csv_gzip', 'parquet', 'parquet_snappy', 'parquet_gz'.
            Defaults to `OutputFormat.CSV_GZIP`. .
        **upload_kwargs (Dict[str, Any]): Additional keyword arguments to pass to
            the underlying `Blob.upload_from_dataframe` method.

    Returns:
        The path that the object was uploaded to.
    """
    gcs_bucket = GcsBucket.load(prefect_gcs_block)

    if isinstance(serialization_format, str):
        serialization_format = DataFrameSerializationFormat[serialization_format.upper()]

    with BytesIO() as bytes_buffer:
        if serialization_format.format == 'parquet':
            df.to_parquet(path=bytes_buffer,
                          compression=serialization_format.compression,
                          index=False)
        elif serialization_format.format == 'csv':
            df.to_csv(path_or_buf=bytes_buffer,
                      compression=serialization_format.compression,
                      index=False)

        bytes_buffer.seek(0)
        to_path = serialization_format.fix_extension_with(gcs_blob_path=to_path)

        return gcs_bucket.upload_from_file_object(
            from_file_object=bytes_buffer,
            to_path=to_path,
            content_type=serialization_format.content_type,
            **upload_kwargs,
        )


@task(log_prints=True, retries=3)
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="Web CSV Dataset to GCS", log_prints=True)
def ingest_csv_to_gcs():
    print("Fetching URL Datasets from .yml")
    datasets: DictConfig = cfg.datasets
    prefect: DictConfig = cfg.prefect

    for dataset_name, endpoints in datasets.items():
        if endpoints is None:
            print(f"Dataset '{dataset_name}' found in config file, "
                  f"but it contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            gcs_path = f"{prefect.gcs_blob_prefix}/{dataset_name}/{filename}"

            raw_df = fetch_csv_from(url=endpoint)
            cleansed_df = fix_datatypes_for(df=raw_df, schema=schemas.get(dataset_name))
            upload_from_dataframe(prefect_gcs_block=prefect.gcs_block_name,
                                  df=cleansed_df,
                                  to_path=gcs_path)


if __name__ == "__main__":
    ingest_csv_to_gcs()
