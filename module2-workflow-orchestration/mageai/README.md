# Workflow orchestration with Mage.ai

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Mage.ai](https://img.shields.io/badge/Mage.ai-0.9-111113?style=flat&logo=apacheairflow&logoColor=white&labelColor=111113)](https://docs.mage.ai/getting-started/setup)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)](https://pandas.pydata.org/docs/user_guide/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This setups the infrastructure for Mage, in Docker, as close as possible to a deploy in a Kubernetes/Helm environment: having a `web_server` and `scheduler` containers, but using a `LocalExecutor` instead.

An additional container `mage_init` sets up this root folder as the main project, and creates a `${MAGE_PROJ_NAME:-magic}` folder for the sub project, so that orchestration across subprojects can also done.


## 🛠️ Getting Started

### Developer Setup (Docker)

**1.** Start setting up the infrastructure in Docker with:
```shell
docker compose up -d
```

**2.** Setting up subprojects:

By default, it sets up a subproject called `magic` where Mage Pipelines can be developed. Additional subprojects can be created by setting up `$MAJ_PROJ_NAME` env var,  followed by and restarting the `mage-init` service: 

```shell
export MAGE_PROJ_NAME=dtc_nyc_taxi
docker compose up -d
```

**3.** Mage UI can be accessed at:
```shell
open http://localhost:6789
```

### Developer Setup (Local)

If a local environment is prefered,

**1.** Install dependencies from pyproject.toml and activate the created virtualenv:
```shell
uv sync && source .venv/bin/activate
```

**2.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**3.** Start Mage in standalone mode:

3.1. Start by starting Postgres and setting the connection URL for mage:
```shell
docker compose up -d ingest-db mage-metastore
export MAGE_DATABASE_CONNECTION_URL=postgresql+psycopg2://mage:mage@localhost:5433/mage
```

3.2. Next, start Mage in Standalone mode
```shell
mage start magic
```

3.3. Mage UI will be accessible at:
```shell
open http://localhost:6789
```


## 📋 TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Code format/lint with Ruff
- [x] Run Mage pipelines on Docker
- [ ] Deploy [Mage to Kubernetes with Helm](https://docs.mage.ai/production/deploying-to-cloud/using-helm)
- [ ] Run/Deploy Mage pipelines on Kubernetes
