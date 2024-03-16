create table demo_test(
    seq_id Int32,
    user_id Int32,
    user_name String,
) engine = ReplacingMergeTree
primary key (seq_id);