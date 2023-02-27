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

                    ______ _ _       _       _____  ____  _      
                   |  ____| (_)     | |     / ____|/ __ \| |     
                   | |__  | |_ _ __ | | __ | (___ | |  | | |     
                   |  __| | | | '_ \| |/ /  \___ \| |  | | |     
                   | |    | | | | | |   <   ____) | |__| | |____ 
                   |_|    |_|_|_| |_|_|\_\ |_____/ \___\_\______|
        
```

## Tech Stack
- PyFlink v1.18.dev0
- FlinkSQL
- JDK 11 
- Jupyter Notebook (EDA)

## Up and Running

### Developer Setup

Install JDK 11. You can do so easily with [SDKMAN!](https://sdkman.io/):

```
$ sdk i java 11.0.18-librca
```

**IMPORTANT NOTES**: 

> **1.** The current version of `apache-flink` for python (1.16.0) depends on `apache-beam==2.35.0`,  
        which is not working properly with Python 3.9, at least not on Mac M1 (aarm64)

> **2.** To workaround these issues, compile Apache Flink and PyFlink from source (1.18-SNAPSHOT). You can find 
         the detailed instructions [here on the official page](https://nightlies.apache.org/flink/flink-docs-master/docs/flinkdev/building/)


### Building Apache Flink and PySpark from Source
- Make sure have `maven at version 3.2.5` installed, otherwise build might fail
- Python must be between 3.7 and 3.10 (inclusive)

```
$ sdk i maven 3.2.5
```

```
$ git clone https://github.com/apache/flink.git
```

```
$ mvn clean install -DskipTests -Dfast -Pskip-webui-build -T 1C
```

```
$ python -m pip install -r flink-python/dev/dev-requirements.txt
```

```
cd flink-python; python setup.py sdist bdist_wheel; cd apache-flink-libraries; python setup.py sdist; cd ..;
```

```
python -m pip install apache-flink-libraries/dist/*.tar.gz
```

```
python -m pip install dist/*.whl
```


## TODO:
- [X] Playground setup for PyFlink
- [x] Explore the Table API to read CSVs
- [x] Explore the FlinkSQL API
