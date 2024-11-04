# NeNo

NeNo (Network Notebooks) is a server and CLI utility that allows you to deploy your jupyter notebooks and trigger their execution
by calling an API endpoint.
You can then use the CLI to view the execution history and inspect the outputs.
Great for scheduled tasks and prototyping APIs.

## Installation

If you want just the CLI utility, you can install it with pip:

```bash
pip install neno
```

Then you can start the utility with `python -m neno`. For convenience, you can create an alias in your shell configuration:

```bash
alias neno="python -m neno"
```

If you want to run the neno server locally, you need to install some optional dependencies:

```bash
pip install "neno[server]"
```

## Launching the server

To start the server, first create a `config.yaml` file:

```yaml
host: "localhost"
port: 5000
backends:
  # For this simple example, we will use the filesystem to store the data and configuration
  dataBackend:
    filesystem:
      path: "backend/data"
  configBackend:
    filesystem:
      path: "backend/config"
```

Then you can start the server with:

```bash
neno serve --config-file config.yaml
```

## Usage

If your server runs somewhere other than `localhost:5000`, point the `NENO_SERVER_URL` environment variable to the correct URL:

```bash
export NENO_SERVER_URL=http://localhost:5001
```

You can then use the CLI to interact with the server:

```bash
# Upload a notebook as a new endpoint. The endpoint will be available at $NENO_SERVER_URL/api/gen-report. We can also use the `--file` option as many times as we want to upload additional files that the notebook needs.
neno add endpoint gen-report --notebook create-report.ipynb --file credentials.json --keep-runs=always

# List all the endpoints
neno get endpoints

# List all endpoints and print a curl command for triggering each one of them
neno get endpoints --show-curl

# List recent executions of the `gen-report` endpoint. By default, it will show the last 10 executions.
neno get runs gen-report

# List last 50 executions of the `gen-report` endpoint
neno get runs gen-report --limit 50

# Download the output (output notebook, any additional files) of the execution of `gen-report` with ID 12345
neno fetch run gen-report 12345

# Download the output of run 12345 and open it in a local jupyterlab instance (jupyterlab must be installed: `pip install jupyterlab`)
neno fetch run gen-report 12345 --inspect
```
