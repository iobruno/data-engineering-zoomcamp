CREATE TABLE demo_test(
    seq_id Int32,
    user_id Int32,
    user_name String,
) ENGINE = ReplacingMergeTree
PRIMARY KEY (seq_id);