# dbt for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.0-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)
![Looker](https://img.shields.io/badge/Looker_Studio-3772FF?style=flat&logo=looker&logoColor=white&labelColor=3772FF)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project focuses on creating dbt models using the NY Taxi Tripdata Datasets in BigQuery. Additionally, it involves developing Dashboards in `Looker Studio` (formerly known as `Google Data Studio`) for data visualizations


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-bigquery](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Looker Studio](https://lookerstudio.google.com/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 / 3.11 with conda:
```shell
conda create -n dbt-bigquery python=3.11 -y
conda activate dbt-bigquery
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
cp profiles.tmpl.yaml ~/.dbt/profiles.yml
```

4.2. Configure the gcp `project_id`, the `dataset`, and `location` where BigQuery should create its tables in (on `profiles.yml`)

```yaml
  method: oauth
  project: iobruno-gcp-labs
  dataset: nyc_trip_record_staging
  location: us-central1
```

4.3. Since we're doing `oauth` authentication for development, run:
```shell
gcloud auth login
```

**5.** Update the `profile` to used by this project on `dbt_project.yml`

Make sure to point to an existing profile name set on profiles.yaml. In this case:
```yaml
profile: 'iobruno-gcp-labs-bigquery'
```

**6.** Run `dbt deps` and `dbt build`:
```shell
dbt deps
dbt build
```

**7.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
```
```shell
dbt docs serve
```

**8.** Access the generated docs on a web browser at the URL:
```shell
open http://localhost:8080
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with BigQuery Adapter
- [x] Generate and serve docs and Data Lineage Graphs locally
- [ ] Run `dbt-core` in Docker
- [ ] Complete dbt Labs Learning Path for `dbt-core`
  - [ ] [dbt Fundamentals](https://courses.getdbt.com/courses/fundamentals)
  - [ ] [Jinja, Macros, Packages](https://courses.getdbt.com/courses/jinja-macros-packages)
  - [ ] [Advanced Materializations](https://courses.getdbt.com/courses/advanced-materializations)
  - [ ] [Refactoring SQL for Modularity](https://courses.getdbt.com/courses/refactoring-sql-for-modularity)
  - [ ] [Analyses and Seeds](https://courses.getdbt.com/courses/analyses-seeds)
  - [ ] [Advanced Testing](https://courses.getdbt.com/courses/advanced-testing)
- [ ] Implement Data Quality metrics it with [dbt-expectations](https://github.com/calogica/dbt-expectations)
- [ ] Implement Data Observability with [elementary-data](https://github.com/elementary-data/elementary)