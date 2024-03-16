create table if not exists demo_test(
    seq_id int,
    user_id int,
    user_name String
) append only;

create sink if not exists demo_test_sink 
from 
    demo_test
with (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = '',
    clickhouse.password = '',
    clickhouse.database = 'default',
    clickhouse.table='demo_test',
);