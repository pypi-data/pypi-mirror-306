# setconfig 🔌

> [!TIP]
> Don't forget to star this repo if you like it! ⭐

Some developers prefer to use `@dataclass` while others prefer `BaseModel`.
This holy war is not going to end soon.
So now they can use the same loader and config file in different parts/microservices of one project.

Currently supported:
- [x] [`@dataclass`](https://docs.python.org/3/library/dataclasses.html)
- [x] Pydantic [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model)
- [x] Python [`SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace) (dotted dict)


## Installation

```bash
pip install setconfig
```


## Usage sample

### Dataclass, full sample [here](examples/example_dataclass.py)

```python
from dataclasses import dataclass
from setconfig import load_config

@dataclass
class Node:
    host: str
    port: int

@dataclass
class Config:
    nodes: list[Node]

config = load_config('config.yaml', into=Config)

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```

### Pydantic, full sample [here](examples/example_pydantic.py)

```python
from pydantic import BaseModel
from setconfig import load_config

class Node(BaseModel):
    host: str
    port: int

class Config(BaseModel):
    nodes: list[Node]

config = load_config('config.yaml', into=Config)

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```

### SimpleNamespace, full sample [here](examples/example_simple.py)

```python
from setconfig import load_config

config = load_config('config.yaml')

print(config)
# >>> Config(nodes=[Node(host='1.1.1.1', port=1000)])
print(config.nodes[0].host)
# >>> '1.1.1.1'
```


## FAQ

### Why only YAML?

> There should be one-- and preferably only one --obvious way to do it
> 
> [(c) Zen of Python](https://peps.python.org/pep-0020/#the-zen-of-python)

### How to load from string/StringIO/etc?

Use `load_config_stream`

```python
from setconfig import load_config_stream

config = load_config_stream('done: true')
```

### I want to use structure from `X` package

Create an issue or PR :)


## More

PyPI: https://pypi.org/project/setconfig

Repository: https://github.com/abionics/setconfig

Developer: Alex Ermolaev (Abionics)

Email: abionics.dev@gmail.com

License: MIT (see LICENSE.txt)
