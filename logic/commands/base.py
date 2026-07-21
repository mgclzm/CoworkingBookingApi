from dataclasses import dataclass
from typing import Any, Generic, TypeVar

CommandResultT = TypeVar("CommandResultT", bound=Any)


@dataclass(frozen=True)
class BaseCommand(Generic[CommandResultT]): ...
