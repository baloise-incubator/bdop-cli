[![Python: 3.10](https://img.shields.io/badge/python-3.10-yellow.svg)](https://www.python.org/downloads/release/python-3108/)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Gitpod](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/baloise-incubator/bdop-cli) 
[![License](https://img.shields.io/github/license/baloise-incubator/bdop-cli?color=lightgrey)](https://github.com/baloise-incubator/bdop-cli/blob/master/LICENSE)

# bdop-cli

bdop-cli is a command line interface (CLI) to perform operations on GitOps managed Baloise DevOps Platform.


## Quick Start
The official bdop-cli container image comes with all dependencies pre-installed and ready-to-use. Pull it with:
```bash
docker pull registry.baloise.dev/bdop-cli
```
Start the CLI and the print the help page with:
```bash
docker run --rm -it registry.baloise.dev/bdop-cli --help
```

## Features
- Update root config repository with all apps from child config repositories.

## Git Provider Support
Currently, we support BitBucket Server, GitHub and Gitlab.

## Development

### Setup

```bash
python3 -m venv venv  # create and activate virtual environment
source venv/bin/activate  # enter virtual environment
make init  # install dependencies, setup dev bdop_cli, install pre-commit hooks, ...
deactivate  # leave virtual environment (after development)
```

### Commands
```bash
make format  # format code
make format-check  # check formatting
make lint  # run linter
make mypy  # run type checks
make test  # run unit tests
make coverage  # run unit tests and create coverage report
make checks  # run all checks (format-check + lint + mypy + test)
make image  # build docker image
make docs  # serves web docs
```

## License
[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)
