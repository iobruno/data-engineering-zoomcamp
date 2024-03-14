CREATE TABLE IF NOT EXISTS demo_test(
    seq_id int,
    user_id int,
    user_name String
) append only;

CREATE SINK IF NOT EXISTS demo_test_sink FROM demo_test
WITH (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = '',
    clickhouse.password = '',
    clickhouse.database = 'default',
    clickhouse.table='demo_test',
);