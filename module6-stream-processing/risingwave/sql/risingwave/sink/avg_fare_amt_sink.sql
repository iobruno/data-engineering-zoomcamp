create sink if not exists avg_fare_amt_sink as 
select 
    avg_fare_amount_per_hour, 
    num_rides_per_hour 
from 
    avg_fare_amt
with (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = '',
    clickhouse.password = '',
    clickhouse.database = 'default',
    clickhouse.table='avg_fare_amt',
    force_append_only = 'true'
);