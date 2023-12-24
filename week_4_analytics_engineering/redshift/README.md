# dbt and Redshift for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.7-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![Redshift](https://img.shields.io/badge/AWS_Redshift-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project focuses on creating dbt models using the NY Taxi Tripdata Datasets in RedShift.

**IMPORTANT NOTE**: To access `awsdatacatalog` from RedShift, IAM auth method is required. It also explicitly needs USAGE grants that DB, therefore, on Redshift Query Editor, run:
```sql
GRANT USAGE ON DATABASE awsdatacatalog to "IAM:my_iam_user";
GRANT ALL ON DATABASE dev to "IAM:my_iam_user";
```


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-redshift](https://docs.getdbt.com/reference/warehouse-setups/redshift-setup)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 / 3.11 with conda:
```shell
conda create -n dbt-redshift python=3.11 -y
conda activate dbt-redshift
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
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
export DBT_REDSHIFT_HOST=hostname.region.redshift-serverless.amazonaws.com \
export DBT_REDSHIFT_DATABASE=dev \
export DBT_REDSHIFT_SCHEMA=nyc_trip_record_data \
export DBT_REDSHIFT_USER=admin \
export DBT_REDSHIFT_PASSWORD="PASSWORD"
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
```
```shell
dbt docs serve
```

**7.** Access the generated docs on a web browser at the URL:
```shell
open http://localhost:8080
```


## Containerization and Testing

**1.** Build the Docker Image with:

```shell
docker build -t dbt_redshift:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run \
  -e DBT_REDSHIFT_HOST=hostname.region.redshift-serverless.amazonaws.com \
  -e DBT_REDSHIFT_DATABASE=dev \
  -e DBT_REDSHIFT_SCHEMA=nyc_trip_record_data \
  -e DBT_REDSHIFT_USER=admin \
  -e DBT_REDSHIFT_PASSWORD="PASSWORD" \
  --name dbt_redshift \
  dbt_redshift
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with Redshift Adapter ([dbt-redshift](https://docs.getdbt.com/docs/core/connect-data-platform/redshift-setup))
- [ ] Generate and serve docs and Data Lineage Graphs locally
- [ ] Run `dbt-core` in Docker