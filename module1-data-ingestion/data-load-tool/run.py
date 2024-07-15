import dlt
import duckdb
from datatalksclub import green_trip_data, yellow_trip_data, fhv_trip_data, zone_lookup_data


def main():
    conn = duckdb.connect("test.db")
    pipeline = dlt.pipeline(
        pipeline_name="dlt-resources-to-duckdb-demo",
        destination=dlt.destinations.duckdb(conn),
        dataset_name='dlt'
    )
    pipeline.run(
        green_trip_data(endpoints=[
            "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-04.csv.gz"
        ])
    )
    print("Finished successfully")


if __name__ == "__main__":
    main()
