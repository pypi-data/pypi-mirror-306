# Waldiez

![CI Build](https://github.com/waldiez/py/actions/workflows/main.yaml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/waldiez/py/badge.svg)](https://coveralls.io/github/waldiez/py) [![PyPI version](https://badge.fury.io/py/waldiez.svg)](https://badge.fury.io/py/waldiez)

Translate a Waldiez flow:

![Flow](https://raw.githubusercontent.com/waldiez/py/refs/heads/main/docs/flow.png)

To a python script or a jupyter notebook with the corresponding [autogen](https://github.com/microsoft/autogen/) agents and chats.

## Features

- Export .waldiez flows to .py or .ipynb
- Run a .waldiez flow
- Include a `logs` folder with the logs of the flow in csv format
- Provide a custom [IOSStream](https://autogen-ai.github.io/autogen/docs/reference/io/base#iostream) to handle input and output.

## Installation

On PyPI:

```bash
python -m pip install waldiez
```

From the repository:

```bash
python -m pip install git+https://github.com/waldiez/py.git
```

## Usage

### CLI

```bash
# Export a Waldiez flow to a python script or a jupyter notebook
waldiez --export /path/to/a/flow.waldiez --output /path/to/an/output/flow[.py|.ipynb]
# Export and run the script, optionally force generation if the output file already exists
waldiez /path/to/a/flow.waldiez --output /path/to/an/output/flow[.py] [--force]
```

### Using docker/podman

```shell
CONTAINER_COMMAND=docker # or podman
# pull the image
$CONTAINER_COMMAND pull waldiez/py
# Export a Waldiez flow to a python script or a jupyter notebook
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.waldiez:/flow.waldiez \
  -v /path/to/an/output:/output \
  waldiez/py --export /flow.waldiez --output /output/flow[.py|.ipynb]

# with selinux and/or podman, you might get permission (or file not found) errors, so you can try:
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.waldiez:/flow.waldiez \
  -v /path/to/an/output:/output \
  --userns=keep-id \
  --security-opt label=disable \
  waldiez/py --export /flow.waldiez --output /output/flow[.py|.ipynb]
```

```shell
# Export and run the script
$CONTAINER_COMMAND run --rm -v /path/to/a/flow.waldiez:/flow.waldiez -v /path/to/an/output:/output waldiez/py /flow.waldiez --output /output/output[.py]
```

### As a library

#### Export a flow

```python
# Export a Waldiez flow to a python script or a jupyter notebook
from waldiez import WaldiezExporter
flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"  # or .ipynb
exporter = WaldiezExporter.load(flow_path)
exporter.export(output_path)
```
  
#### Run a flow

```python
# Run a flow
from waldiez import WaldiezRunner
flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"
runner = WaldiezRunner.load(flow_path)
runner.run(output_path=output_path)
```

#### Run a flow with a custom IOStream

```python
# Run the flow with a custom IOStream
from waldiez import WaldiezRunner
from waldiez.io import WaldiezIOStream

flow_path = "/path/to/a/flow.waldiez"
output_path = "/path/to/an/output.py"

def print_function(*values, **args) -> None:
    """A custom print function."""
    print(values)

def on_prompt_input(prompt: str) -> str:
    """A custom input function."""
    return input(prompt)

io_stream = WaldiezIOStream(
    print_function=print_function,
    on_prompt_input=on_prompt_input,
    input_timeout=30,
)
with WaldiezIOStream.set_default(io_stream):
    runner = WaldiezRunner.load(flow_path)
    runner.run(stream=io_stream, output_path=output_path)

io_stream.close()

```

### Tools

- [autogen](https://github.com/microsoft/autogen/)
- [juptytext](https://github.com/mwouts/jupytext)
- [twisted](https://github.com/twisted/twisted)
- [pydantic](https://github.com/pydantic/pydantic)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/waldiez/py/blob/main/LICENSE) file for details.
