"""
Developed by Alex Ermolaev (Abionics)
Email: abionics.dev@gmail.com
License: MIT
"""

__version__ = '1.3.1'

from dataclasses import is_dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import TypeVar, Type, Any

import yaml
from dacite import from_dict, Config
from pydantic import BaseModel

T = TypeVar('T')


def load_config(
        path: Path | str = 'config.yaml',
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    with open(path, 'r') as file:
        data = yaml.safe_load(file) or ''
    return load_config_dict(data, into, override, **kwargs)


def load_config_stream(
        stream: Any,
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    data = yaml.safe_load(stream)
    return load_config_dict(data, into, override, **kwargs)


def load_config_dict(
        data: dict,
        into: Type[T] | None = None,
        override: dict | None = None,
        **kwargs,
) -> T:
    if override:
        data = data | override
    if isinstance(into, SimpleNamespace) or into is None:
        return parse_simple(data)
    if is_dataclass(into):
        config = Config(**kwargs)
        return from_dict(into, data, config)  # type: ignore
    if issubclass(into, BaseModel):
        return into.model_validate(data, **kwargs)  # type: ignore
    raise TypeError(f'Unsupported output class: {into}')


def parse_simple(data: Any) -> Any:
    if isinstance(data, dict):
        parsed = {
            str(key): parse_simple(value)
            for key, value in data.items()
        }
        return SimpleNamespace(**parsed)
    if isinstance(data, list | tuple):
        return data.__class__((
            parse_simple(item)
            for item in data
        ))
    return data
