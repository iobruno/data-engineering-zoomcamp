# dbt and Redshift for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.12_|_3.11_|_3.10-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.8-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![Redshift](https://img.shields.io/badge/AWS_Redshift-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-redshift` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique.

**IMPORTANT NOTE**: To access `awsdatacatalog` from RedShift, IAM auth method is required. It also explicitly needs USAGE grants that DB, therefore, on Redshift Query Editor, run:
```sql
GRANT USAGE ON DATABASE awsdatacatalog to "IAM:my_iam_user";
GRANT ALL ON DATABASE <DATABASE_NAME> to "IAM:my_iam_user";
```

## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-redshift](https://docs.getdbt.com/reference/warehouse-setups/redshift-setup)
- [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/)

## Up and Running

### Developer Setup

**1.** Install the dependencies on `pyproject.toml`:
```shell
uv sync
```

**2.** Activate the virtualenv created by `uv`:
```shell
source .venv/bin/activate
```

**3. (Optional)**  Install pre-commit:
```shell
brew install pre-commit
```

From root folder where `.pre-commit-config.yaml` is located, run:
```shell
pre-commit install
```

**4.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yaml` as template)

4.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

4.2. Set the environment variables for `dbt-bigquery`:
```shell
export DBT_REDSHIFT_HOST=redshift.[id].[region].redshift-serverless.amazonaws.com
export DBT_REDSHIFT_DATABASE=dev
export DBT_REDSHIFT_USE_DATA_CATALOG=1
export DBT_REDSHIFT_SOURCE_GLUE_CATALOG_DB=raw_nyc_tlc_tripdata
export DBT_REDSHIFT_TARGET_SCHEMA=nyc_tlc_record_data
```

4.3. Also, either have your AWS credentials set on `~/.aws/credentials` or set them as well:
```shell
export AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
```

**5.** Install dbt dependencies and trigger the pipeline

5.1. Run `dbt deps` to install  dbt plugins
```shell
dbt deps
```

5.2. Run `dbt seed` to push/create the tables from the .csv seed files to the target schema
```shell
dbt seed
```

5.3. Run dbt run to trigger the dbt models to run
```shell
dbt build

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+
```

**6.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
dbt docs serve
```

Access the generated docs at:
```shell
open http://localhost:8080
```

## Containerization and Testing

**1.** Build the Docker Image with:

```shell
docker build -t dbt-redshift:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e DBT_REDSHIFT_HOST=${DBT_REDSHIFT_HOST} \
  -e DBT_REDSHIFT_DATABASE=dev \
  -e DBT_REDSHIFT_USE_DATA_CATALOG=1 \
  -e DBT_REDSHIFT_SOURCE_GLUE_CATALOG_DB=raw_nyc_tlc_tripdata \
  -e DBT_REDSHIFT_TARGET_SCHEMA=nyc_tlc_record_data \
  --name dbt-redshift \
  dbt-redshift
```

## TODO:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with Redshift Adapter ([dbt-redshift](https://docs.getdbt.com/docs/core/connect-data-platform/redshift-setup))
- [x] Add dbt macro to configure target schemas dinamically
- [x] Run `dbt-core` in Docker
- [ ] Terraform AWS Glue Catalog and Crawler
