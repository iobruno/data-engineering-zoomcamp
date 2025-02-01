# StarRocks
![StarRocks](https://img.shields.io/badge/StarRocks-3.4-FABF00?style=flat&logo=apachespark&logoColor=FABF00&labelColor=1B1F21)
![MinIO](https://img.shields.io/badge/MinIO-00091B?style=flat&logo=minio&logoColor=CF163D&labelColor=00091B)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Up and Running

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

## TODO:
- [x] Setup `StarRocks-FE` on Docker compose
- [x] Setup `StarRocks-CN` and `S3/MinIO` for Federated Queries on Object Storage
- [ ] Ingestion script for StarRocks
