# Data Observability with PipeRider, dbt, and DuckDB Project:

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.0-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![DuckDB](https://img.shields.io/badge/DuckDB-black?style=flat&logo=duckdb&logoColor=FEF000&labelColor=black)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

Data observability with dbt, DuckDB, and PipeRider. This project focuses on building a dbt model on DuckDB and integrating PipeRider pipelines for robust data observability.


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

**3.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yaml` as template)

3.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
cp profiles.tmpl.yaml ~/.dbt/profiles.yml
```

3.2. Configure the `gcp project_id` and the local `path` where duckdb should save its file (on `profiles.yml`)

```yaml
  path: '/tmp/piperider.duckdb'
  filesystems:
  - fs: gcs
    project: iobruno-gcp-labs
```

3.3. Make sure the `GOOGLE_APPLICATION_CREDENTIALS` env variable is set
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp-credentials.json
```

**4.** Update the `profile` to used by this project on `dbt_project.yml`

Make sure to point to an existing profile name set on profiles.yaml. In this case:
```yaml
profile: 'duckdb-local'
```

**5.** Run `dbt deps` and `dbt build`:
```shell
dbt deps
dbt build
```

**6.** Initialize the PipeRider setup and run it for the first time:
```shell
piperider init 
piperider run
```

**7. (Optional)**  Install pre-commit:
```shell
brew install pre-commit
```

From root folder where `.pre-commit-config.yaml` is located, run:
```shell
pre-commit install
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with DuckDB Adapter
- [x] Integrate with PipeRider and generate reports
- [x] Modify the dbt models, generate a new report and compare
- [x] Utilize the comparison on a [GitHub Pull Request](https://github.com/iobruno/data-engineering-zoomcamp/pull/2)
- [ ] Set up a CI Pipeline with GitHub Actions