# Flink for Batch Processing Pipelines

This subproject builds `pyflink` playground to develop Batch Processing Pipeline Playground for `NY Taxi Tripdata Datasets`

```

                                   ▒▓██▓██▒
                               ▓████▒▒█▓▒▓███▓▒
                            ▓███▓░░        ▒▒▒▓██▒  ▒
                          ░██▒   ▒▒▓▓█▓▓▒░      ▒████
                          ██▒         ░▒▓███▒    ▒█▒█▒
                            ░▓█            ███   ▓░▒██
                              ▓█       ▒▒▒▒▒▓██▓░▒░▓▓█
                            █░ █   ▒▒░       ███▓▓█ ▒█▒▒▒
                            ████░   ▒▓█▓      ██▒▒▒ ▓███▒
                         ░▒█▓▓██       ▓█▒    ▓█▒▓██▓ ░█░
                   ▓░▒▓████▒ ██         ▒█    █▓░▒█▒░▒█▒
                  ███▓░██▓  ▓█           █   █▓ ▒▓█▓▓█▒
                ░██▓  ░█░            █  █▒ ▒█████▓▒ ██▓░▒
               ███░ ░ █░          ▓ ░█ █████▒░░    ░█░▓  ▓░
              ██▓█ ▒▒▓▒          ▓███████▓░       ▒█▒ ▒▓ ▓██▓
           ▒██▓ ▓█ █▓█       ░▒█████▓▓▒░         ██▒▒  █ ▒  ▓█▒
           ▓█▓  ▓█ ██▓ ░▓▓▓▓▓▓▓▒              ▒██▓           ░█▒
           ▓█    █ ▓███▓▒░              ░▓▓▓███▓          ░▒░ ▓█
           ██▓    ██▒    ░▒▓▓███▓▓▓▓▓██████▓▒            ▓███  █
          ▓███▒ ███   ░▓▓▒░░   ░▓████▓░                  ░▒▓▒  █▓
          █▓▒▒▓▓██  ░▒▒░░░▒▒▒▒▓██▓░                            █▓
          ██ ▓░▒█   ▓▓▓▓▒░░  ▒█▓       ▒▓▓██▓    ▓▒          ▒▒▓
          ▓█▓ ▓▒█  █▓░  ░▒▓▓██▒            ░▓█▒   ▒▒▒░▒▒▓█████▒
           ██░ ▓█▒█▒  ▒▓▓▒  ▓█                █░      ░░░░   ░█▒
           ▓█   ▒█▓   ░     █░                ▒█              █▓
            █▓   ██         █░                 ▓▓        ▒█▓▓▓▒█░
             █▓ ░▓██░       ▓▒                  ▓█▓▒░░░▒▓█░    ▒█
              ██   ▓█▓░      ▒                    ░▒█▒██▒      ▓▓
               ▓█▒   ▒█▓▒░                         ▒▒ █▒█▓▒▒░░▒██
                ░██▒    ▒▓▓▒                     ▓██▓▒█▒ ░▓▓▓▓▒█▓
                  ░▓██▒                          ▓░  ▒█▓█  ░░▒▒▒
                      ▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▓▓  ▓░▒█░

    ______ _ _       _       _____  ____  _         _____ _ _            _  BETA
   |  ____| (_)     | |     / ____|/ __ \| |       / ____| (_)          | |
   | |__  | |_ _ __ | | __ | (___ | |  | | |      | |    | |_  ___ _ __ | |_
   |  __| | | | '_ \| |/ /  \___ \| |  | | |      | |    | | |/ _ \ '_ \| __|
   | |    | | | | | |   <   ____) | |__| | |____  | |____| | |  __/ | | | |_
   |_|    |_|_|_| |_|_|\_\ |_____/ \___\_\______|  \_____|_|_|\___|_| |_|\__|

        Welcome! Enter 'HELP;' to list all available commands. 'QUIT;' to exit.


Flink SQL>
```

## Tech Stack
- Python 3.10 / 3.9
- JDK 11
- PyFlink v1.18.dev0 (Python API for Flink)
- Flink SQL
- Jupyter Notebook (EDA)
- [Poetry](https://python-poetry.org/docs/)

## Up and Running

### Developer Setup

**1.** Install JDK 11. You can do so easily with [SDKMAN!](https://sdkman.io/):

```
$ sdk i java 11.0.18-librca
```

**2.** Build Apache Flink and PyFlink from Source

**IMPORTANT NOTES:**

> **1.** The current version of `apache-flink` for python (1.16.0) depends on `apache-beam==2.35.0`,
        which is not working properly with Python 3.9, at least not on Mac M1 (aarm64)

> **2.** To workaround these issues, compile Apache Flink and PyFlink from source (1.18-SNAPSHOT). You can find
         the detailed instructions [here on the official page](https://nightlies.apache.org/flink/flink-docs-master/docs/flinkdev/building/)


- Make sure have `maven at version 3.2.5` installed, otherwise build might fail
- Python must be between 3.7 and 3.10 (inclusive)

```shell
sdk i maven 3.2.5
```

```shell
git clone https://github.com/apache/flink.git
```

```shell
mvn clean install -DskipTests -Dfast -Pskip-webui-build -T 1C
```

```shell
python -m pip install -r flink-python/dev/dev-requirements.txt
```

```shell
cd flink-python; python setup.py sdist bdist_wheel; cd apache-flink-libraries; python setup.py sdist; cd ..;
```

```shell
python -m pip install apache-flink-libraries/dist/*.tar.gz
```

```shell
python -m pip install dist/*.whl
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit
```

## TODO:
- [x] Set up a Jupyter Playground for PyFlink
- [x] Explore Flink's Table API to read CSVs
- [x] Explore the FlinkSQL API
- [ ] Set up a Standalone Cluster for Flink
- [ ] Submit a PyFlink job to the Cluster
