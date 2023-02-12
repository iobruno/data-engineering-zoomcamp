from pathlib import Path
from typing import Dict, Any, Union

import pandas as pd
from omegaconf import OmegaConf
from io import BytesIO
from prefect_gcp import GcsBucket

from prefect import flow, task
from enum import Enum

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
cfg = OmegaConf.load(config_file)


class OutputFormat(Enum):
    """An enumeration class to represent different file formats,
        compression options for upload_from_dataframe

    Class Attributes:
        CSV (tuple): Representation for 'csv' file format with no compression
            and its related content type and suffix.

        CSV_GZIP (tuple): Representation for 'csv' file format with 'gzip' compression
            and its related content type and suffix.

        PARQUET (tuple): Representation for 'parquet' file format with no compression
            and its related content type and suffix.

        PARQUET_SNAPPY (tuple): Representation for 'parquet' file format
            with 'snappy' compression and its related content type and suffix.

        PARQUET_GZIP (tuple): Representation for 'parquet' file format
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

    @classmethod
    def lookup(cls, output_format: str):
        """
        Returns the instance of the class that corresponds to the input `fmt`.
        If no match is found, returns `CSV_GZIP` as a default value.

        Parameters:
            output_format (str): The string representation of the file format.

        Returns:
            OutputFormat: The instance of the class that corresponds to `fmt`.
        """
        lookup_table = {f'{entry.name}': entry for entry in OutputFormat}
        return lookup_table.get(output_format.upper(), OutputFormat.CSV_GZIP)


@task(log_prints=True)
def upload_from_dataframe(prefect_gcs_block: str,
                          df: pd.DataFrame,
                          to_path: str,
                          output_format: Union[str, OutputFormat] = OutputFormat.PARQUET_SNAPPY,
                          **upload_kwargs: Dict[str, Any]):
    """Upload a Pandas DataFrame to Google Cloud Storage in various formats.

    This function uploads the data in a Pandas DataFrame to Google Cloud Storage
    in a specified format, such as .csv, .csv.gz, .parquet, .parquet.snappy, and .parquet.gz.

    Args:
        prefect_gcs_block (str): The Prefect GcsBlock name
        df (pd.DataFrame): The Pandas DataFrame to be uploaded.
        to_path (str): The destination path for the uploaded DataFrame.
        output_format (Union[str, OutputFormat]): The format to serialize the DataFrame into.
            Defaults to `OutputFormat.CSV_GZIP`. When passed as a `str`, the valid options are:
            'csv', 'csv_gzip', 'parquet', 'parquet_snappy', 'parquet_gz'.
        **upload_kwargs (Dict[str, Any]): Additional keyword arguments to pass to the underlying
            `Blob.upload_from_dataframe` method.

    Returns:
        None
    """
    gcs_bucket = GcsBucket.load(prefect_gcs_block)

    def fix_extension_with(gcs_blob: str, ext: str):
        """Fix the extension of a GCS blob.

        Args:
            gcs_blob (str): The path to the GCS blob to be modified.
            ext (str): The extension to add to the filename.

        Returns:
            str: The modified path to the GCS blob with the new extension.
        """
        gcs_blob = Path(gcs_blob)
        folder, filename = (
            gcs_blob.parent,
            Path(gcs_blob.stem).with_suffix(ext)
        )
        return folder.joinpath(filename)

    if type(output_format) == str:
        output_format = OutputFormat.lookup(output_format)

    with BytesIO() as bytes_buffer:
        if output_format.format == 'parquet':
            df.to_parquet(path=bytes_buffer, compression=output_format.compression, index=False)
        elif output_format.format == 'csv':
            df.to_csv(path_or_buf=bytes_buffer, compression=output_format.compression, index=False)

        bytes_buffer.seek(0)
        to_path = fix_extension_with(to_path, output_format.suffix)
        return gcs_bucket.upload_from_file_object(
            from_file_object=bytes_buffer,
            to_path=to_path,
            content_type=output_format.content_type,
            **upload_kwargs,
        )


@task(log_prints=True, retries=3)
def fix_datatypes_for(df: pd.DataFrame) -> pd.DataFrame:
    return df.astype({
        'PUlocationID': 'Int64',
        'DOlocationID': 'Int64',
        'SR_Flag': 'Int64'
    })


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="NYC FHV Trip Data Dataset to GCS", log_prints=True)
def ingest_csv_to_gcs():
    try:
        print("Fetching URL Datasets from .yml")
        datasets = cfg.datasets
        if datasets.fhv:
            for endpoint in datasets.fhv:
                raw_df = fetch_csv_from(url=endpoint)
                cleansed_df = fix_datatypes_for(df=raw_df)
                upload_from_dataframe(prefect_gcs_block="gcs-dtc-datalake-raw",
                                      df=cleansed_df,
                                      to_path=f"fhv/parquet_snappy/{Path(endpoint).name}",
                                      output_format='parquet_snappy')
    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest_csv_to_gcs()
