# dbt and DuckDB for Data Reliability

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.7-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![DuckDB](https://img.shields.io/badge/DuckDB-black?style=flat&logo=duckdb&logoColor=FEF000&labelColor=black)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-duckdb` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique. 

It also adds Data Reliability on top of that with PipeRider.

## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-duckdb](https://docs.getdbt.com/reference/warehouse-setups/duckdb-setup)
- [PipeRider](https://github.com/InfuseAI/piperider)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 / 3.11 with conda:
```shell
conda create -n dbt-duckdb python=3.11 -y
conda activate dbt-duckdb
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

**4.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yml` as template)

4.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

4.2. Set the environment variables for `dbt-bigquery`:

```shell
export DBT_DUCKDB_GCS_PATH=
export DBT_DUCKDB_TARGET_FILE=
```

4.3. Since we're doing `oauth` authentication for development, run:
```shell
gcloud auth login
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
Access the generated docs at:
```shell
open http://localhost:8080
```

**7.** Setup and run PipeRider:

```shell
piperider init 
```
```shell
piperider diagnose
```
The output should be similar to:
```shell
Diagnosing...

Check format of data sources:
  dev: [OK]
✅ PASS

Check connections:
  DBT: [OK]
    Version: 1.7.2
    Adapter: duckdb
    Profile: duckdb-local
    Target:  dev 
  Name: dev
  Type: duckdb
  Connector: [OK]
  Connection: [OK]
✅ PASS

🎉 You are all set!
```

Finally, run piperider itself:
```shell
piperider run
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with DuckDB Adapter ([dbt-duckdb](https://github.com/duckdb/dbt-duckdb))
- [x] Configure [dbt-duckdb](https://github.com/duckdb/dbt-duckdb) to use `fsspec` and [read directly from GCS](https://gcsfs.readthedocs.io/en/latest/api.html?highlight=GCSFileSystem#gcsfs.core.GCSFileSystem)
- [x] Integrate with PipeRider and generate reports
- [x] Modify the dbt models, generate a new report and compare
- [x] Utilize the comparison on a [GitHub Pull Request](https://github.com/iobruno/data-engineering-zoomcamp/pull/2)
- [ ] Set up a CI Pipeline with GitHub Actions