# Introduction

This folder comprises is the energy data and calculation microservice for TIP. It contains the Python module that is used to interface with the ETM, using the API asynchrounously. It's called `Hail` because it makes it rain ETM-requests :cloud_with_lightning_and_rain: :cloud_with_lightning_and_rain:.

## Installation

To install TIP, follow these steps:

### Minimal: Poetry

1. Make sure you have [Poetry](https://python-poetry.org/) installed on your system.
2. Clone the repository using `git clone`
3. Navigate to the project directory: `cd pMIEK-tool`
4. Install the dependencies: `poetry install`
5. Activate the virtual environment: `poetry shell`

You can now run Python files using Poetry. If you want to run the microservice (`app.py`) then set the `NO_CACHE` variable to `1` in your OS enviroment variables and use `fastapi dev app.py`.

### Dev container

If you prefer to use Visual Studio Code (VSCode) instead, follow these steps:

1. Install [VSCode](https://code.visualstudio.com/) on your system.
2. Clone the repository using `git clone`
3. Open the project directory in VSCode: `code pMIEK-tool`
4. Install the `Dev Containers` extension in VSCode
5. Reopen the window in container using `CTRL + SHIFT + P` > "Dev Containers: Reopen in container"
6. Browse `localhost:7000/docs` to see the FastAPI docs

### Production build

To trigger builds to production, you can use the `production` branch on Azure Repos. However, if you want to mimic it locally, you can use `docker compose up`. Just make sure to set the required OS environment variables beforehand.

### Configuration

Inputs can be configured in the `config` folder. All needed files and corresponding meta data is already there. Just type equations as if you are doing simple arithmatic and `hail` will handle all API-calls, statemanagement and matrix calculations under the hood.

### Updating references

Since the configuration, the ETM API and the available outputs in this application are heavily intertwined, the reference to between all these elements can be automatically updated using the `poetry run update-refs` command. This will trigger a script that uses Jinja templating to automatically generate type hints and hard references. The type hints are only used statically (not at runtime), making configuration easier by allowing for autocompletion of queries and input elements available on the ETM. The hard references are used at runtime for configuration specific logic and to list all available results.

Typically, you would only need to run `poetry run update-refs -r` if you add new result configuration and `poetry run update-refs -d` for developments, respectively. Only if you miss type hints for a specific ETM API key, you'd want to rerun `poetry run update-refs --etm`.

N.b., flags can be combined. E.g. `poetry run update-refs -r -d`. Not providing flags is shorthand for updating all.

For help, run:

```python
poetry run update-refs --help
```

## API spec and docs

Browse `localhost:7000/docs` to see the FastAPI docs, with OpenAPI schemas and a playground for each endpoint.

### Palettes

Maps use `colorcet` (https://colorcet.holoviz.org/) for perceptually accurate 256-color colormaps. To visually browse these palettes, navigate to http://localhost:7000/browse_palettes; this will display all valid colormaps that can be used.

## Known posibilities for optimisation

1. Implement one Redis-client per request instead of at least 2 clients per ETM-scenario (`cache.py`, `app.py` and `client.py`)
2. Every requests loads the classes (might be pycached) from the `config`, this could be done once on application startup (`generate.py`)

## Performance eval

### Import time

```
time python dev.py
```

```
python -X importtime dev.py 2>&1 | grep 'import time:' | sort -k 3 -n
```

### Loads of calls

Use `app.pushit.py`. Or time things using `cProfile` or alternative.

## Tests

```shell
poetry run pytest
```
