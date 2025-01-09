# StarRocks Query Engine
[![StarRocks](https://img.shields.io/badge/StarRocks-3.4-FABF00?style=flat&logo=lightning&logoColor=white&labelColor=262A38)](https://docs.starrocks.io/docs/introduction/StarRocks_intro/)
[![MinIO](https://img.shields.io/badge/MinIO-00091B?style=flat&logo=minio&logoColor=CF163D&labelColor=00091B)](https://min.io/docs/minio/container)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Getting Started

1. Spin the infrastructure with:
```shell
docker compose up -d
```

2. Ensure the following services are up and running:
- starrocks-fe
- starrocks-cn
- metastore
- metastore-db
- minio


## TODO's:
- [x] Setup `StarRocks-FE` on Docker compose
- [x] Setup `StarRocks-CN` and `S3/MinIO` for Federated Queries on Object Storage
- [ ] Ingestion script for StarRocks
