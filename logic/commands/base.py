from dataclasses import dataclass
from abc import ABC
from typing import Any, Generic, TypeVar

CommandResultT = TypeVar('CommandResultT', bound=Any)

@dataclass(frozen=True)
class BaseCommand(Generic[CommandResultT]):
    ...

