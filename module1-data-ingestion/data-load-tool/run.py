import dlt
import duckdb
import datatalksclub as dtc
from github import releases as gh_releases


def main():
    conn = duckdb.connect("test.db")
    pipeline = dlt.pipeline(
        pipeline_name="dlt-resources-to-duckdb-demo",
        destination=dlt.destinations.duckdb(conn),
        dataset_name='dlt'
    )

    source = gh_releases(owner="DataTalksClub", repo="nyc-tlc-data")
    pipeline.run(
        source.download_links_group_by("tag_name")
        | dtc.process_datasets
        | print,
        write_disposition='replace'
    )


if __name__ == "__main__":
    main()

