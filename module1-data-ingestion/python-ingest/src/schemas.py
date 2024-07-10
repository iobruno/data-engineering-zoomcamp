from abc import ABCMeta, abstractmethod
import polars as pl


class Schema(metaclass=ABCMeta):
    @property
    @abstractmethod
    def polars(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def pyarrow(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def rename_to(self):
        raise NotImplementedError()


class GreenTaxiSchema(Schema):
    @property
    def polars(self):
        return {
            "VendorID": pl.Int32,
            "lpep_pickup_datetime": pl.Datetime,
            "lpep_dropoff_datetime": pl.Datetime,
            "passenger_count": pl.Int8,
            "trip_distance": pl.Float64,
            "PULocationID": pl.Int32,
            "DOLocationID": pl.Int32,
            "RatecodeID": pl.Int8,
            "store_and_fwd_flag": pl.String,
            "payment_type": pl.Int8,
            "fare_amount": pl.Float64,
            "extra": pl.Float64,
            "mta_tax": pl.Float64,
            "improvement_surcharge": pl.Float64,
            "tip_amount": pl.Float64,
            "tolls_amount": pl.Float64,
            "total_amount": pl.Float64,
            "congestion_surcharge": pl.Float64,
            "ehail_fee": pl.Float64,
            "trip_type": pl.Int8,
        }

    @property
    def pyarrow(self):
        return {
            "VendorID": "Int64",
            "lpep_pickup_datetime": "datetime64[s]",
            "lpep_dropoff_datetime": "datetime64[s]",
            "passenger_count": "Int64",
            "trip_distance": "float64",
            "PULocationID": "Int64",
            "DOLocationID": "Int64",
            "RatecodeID": "Int64",
            "store_and_fwd_flag": "string",
            "payment_type": "Int64",
            "fare_amount": "float64",
            "extra": "float64",
            "mta_tax": "float64",
            "improvement_surcharge": "float64",
            "tip_amount": "float64",
            "tolls_amount": "float64",
            "total_amount": "float64",
            "congestion_surcharge": "float64",
            "ehail_fee": "float64",
            "trip_type": "Int64",
        }

    @property
    def rename_to(self):
        return {
            "VendorID": "vendor_id",
            "lpep_pickup_datetime": "lpep_pickup_datetime",
            "lpep_dropoff_datetime": "lpep_dropoff_datetime",
            "passenger_count": "passenger_count",
            "trip_distance": "trip_distance",
            "PULocationID": "pu_location_id",
            "DOLocationID": "do_location_id",
            "RatecodeID": "ratecode_id",
            "store_and_fwd_flag": "store_and_fwd_flag",
            "payment_type": "payment_type",
            "fare_amount": "fare_amount",
            "extra": "extra",
            "mta_tax": "mta_tax",
            "improvement_surcharge": "improvement_surcharge",
            "tip_amount": "tip_amount",
            "tolls_amount": "tolls_amount",
            "total_amount": "total_amount",
            "congestion_surcharge": "congestion_surcharge",
            "ehail_fee": "ehail_fee",
            "trip_type": "trip_type",
        }


class YellowTaxiSchema(Schema):
    @property
    def polars(self):
        return {
            "VendorID": pl.Int32,
            "tpep_pickup_datetime": pl.Datetime,
            "tpep_dropoff_datetime": pl.Datetime,
            "passenger_count": pl.Int8,
            "trip_distance": pl.Float64,
            "PULocationID": pl.Int32,
            "DOLocationID": pl.Int32,
            "RatecodeID": pl.Int8,
            "store_and_fwd_flag": pl.String,
            "payment_type": pl.Int8,
            "fare_amount": pl.Float64,
            "extra": pl.Float64,
            "mta_tax": pl.Float64,
            "improvement_surcharge": pl.Float64,
            "tip_amount": pl.Float64,
            "tolls_amount": pl.Float64,
            "total_amount": pl.Float64,
            "congestion_surcharge": pl.Float64,
        }

    @property
    def pyarrow(self):
        return {
            "VendorID": "Int64",
            "tpep_pickup_datetime": "datetime64[s]",
            "tpep_dropoff_datetime": "datetime64[s]",
            "passenger_count": "Int64",
            "trip_distance": "float64",
            "PULocationID": "Int64",
            "DOLocationID": "Int64",
            "RatecodeID": "Int64",
            "store_and_fwd_flag": "string",
            "payment_type": "Int64",
            "fare_amount": "float64",
            "extra": "float64",
            "mta_tax": "float64",
            "improvement_surcharge": "float64",
            "tip_amount": "float64",
            "tolls_amount": "float64",
            "total_amount": "float64",
            "congestion_surcharge": "float64",
        }

    @property
    def rename_to(self):
        return {
            "VendorID": "vendor_id",
            "tpep_pickup_datetime": "tpep_pickup_datetime",
            "tpep_dropoff_datetime": "tpep_dropoff_datetime",
            "passenger_count": "passenger_count",
            "trip_distance": "trip_distance",
            "PULocationID": "pu_location_id",
            "DOLocationID": "do_location_id",
            "RatecodeID": "ratecode_id",
            "store_and_fwd_flag": "store_and_fwd_flag",
            "payment_type": "payment_type",
            "fare_amount": "fare_amount",
            "extra": "extra",
            "mta_tax": "mta_tax",
            "improvement_surcharge": "improvement_surcharge",
            "tip_amount": "tip_amount",
            "tolls_amount": "tolls_amount",
            "total_amount": "total_amount",
            "congestion_surcharge": "congestion_surcharge",
        }


class FhvSchema(Schema):
    @property
    def polars(self):
        return {
            "dispatching_base_num": pl.String,
            "pickup_datetime": pl.String,
            "dropOff_datetime": pl.String,
            "PUlocationID": pl.Int32,
            "DOlocationID": pl.Int32,
            "SR_Flag": pl.String,
            "Affiliated_base_number": pl.String,
        }

    @property
    def pyarrow(self):
        return {
            "dispatching_base_num": "string",
            "pickup_datetime": "datetime64[s]",
            "dropOff_datetime": "datetime64[s]",
            "PUlocationID": "Int64",
            "DOlocationID": "Int64",
            "SR_Flag": "string",
            "Affiliated_base_number": "string",
        }

    @property
    def rename_to(self):
        return {
            "dispatching_base_num": "dispatching_base_num",
            "pickup_datetime": "pickup_datetime",
            "dropOff_datetime": "dropoff_datetime",
            "PUlocationID": "pu_location_id",
            "DOlocationID": "do_location_id",
            "SR_Flag": "sr_flag",
            "Affiliated_base_number": "affiliated_base_number",
        }


class ZoneLookupSchema(Schema):
    @property
    def polars(self):
        return {
            "LocationID": pl.Int32,
            "Borough": pl.String,
            "Zone": pl.String,
            "service_zone": pl.String,
        }

    @property
    def pyarrow(self):
        return {
            "LocationID": "Int64",
            "Borough": "string",
            "Zone": "string",
            "service_zone": "string",
        }

    @property
    def rename_to(self):
        return {
            "LocationID": "location_id",
            "Borough": "borough",
            "Zone": "zone",
            "service_zone": "service_zone",
        }
