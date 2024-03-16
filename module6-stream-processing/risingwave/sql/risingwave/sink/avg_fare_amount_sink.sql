create sink if not exists avg_fare_amout_sink as 
select 
    avg_fare_amount_per_hour, 
    num_rides_per_hour 
from 
    avg_fare_amount
with (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = 'clickhouse',
    clickhouse.password = 'clickhouse',
    clickhouse.database = 'default',
    clickhouse.table='avg_fare_amount',
    force_append_only = 'true'
);