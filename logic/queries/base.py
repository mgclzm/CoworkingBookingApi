from abc import ABC
from typing import Generic, TypeVar

ResultT = TypeVar('ResultT')

class BaseQuery(ABC, Generic[ResultT]):
    ...