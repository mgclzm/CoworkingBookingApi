from dataclasses import dataclass
from abc import ABC, abstractmethod

class BaseEntity:
    ...

class ApplicationException(ABC, BaseException):
    ...
    @property
    @abstractmethod
    def message(self) -> str:
        ...

@dataclass
class InactiveEntityUsageError(ApplicationException):
    entity: BaseEntity

    @property
    def message(self) -> str:
        return f'Inactive usage of {type(self.entity)} entity'
    
class LogicException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        ...