from abc import ABC
from typing import Generic, TypeVar

ResultT = TypeVar(name='ResultT')

class BaseQuery(ABC, Generic[ResultT]):
    ...