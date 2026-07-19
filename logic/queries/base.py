from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

QueryResultT = TypeVar('QueryResultT', bound=Any)

@dataclass(frozen=True)
class BaseQuery(Generic[QueryResultT]):
    ...

