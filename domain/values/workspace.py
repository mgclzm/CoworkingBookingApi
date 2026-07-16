from dataclasses import dataclass
from datetime import time

from domain.entities.base import ApplicationException

@dataclass
class InvalidTitleError(ApplicationException):
    title_value: str

    @property
    def message(self) -> str:
        return f'Title value cannot be empty or bigger then 50 characters, got {self.title_value}'

@dataclass
class InvalidNumberError(ApplicationException):
    number_value: int

    @property
    def message(self) -> str:
        return f'Spot number must be between 1 and 100, got {self.number_value}'

@dataclass
class InvalidWorkingTimeError(ApplicationException):
    opening_time: time
    closing_time: time

    @property
    def message(self) -> str:
        return f'Opening time must be before closing time, got opening time = {self.opening_time}, closing time = {self.closing_time}'

@dataclass
class InvalidDescriptionError(ApplicationException):
    description_value: str

    @property
    def message(self) -> str:
        return f'Workspace description must me less then 1000, actual length {len(self.description_value)}'

@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not self.value.strip() or len(self.value) > 50:
            raise InvalidTitleError(self.value)

@dataclass(frozen=True)
class Number:
    value: int

    def __post_init__(self):
        if self.value <= 0 or self.value > 100:
            raise InvalidNumberError(self.value)
        
@dataclass(frozen=True)
class WorkingTime:
    opening_time: time
    closing_time: time

    def __post_init__(self):
        if self.opening_time >= self.closing_time:
            raise InvalidWorkingTimeError(opening_time=self.opening_time, closing_time=self.closing_time)
        
@dataclass(frozen=True)
class WorkspaceDescription: 
    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise InvalidDescriptionError(self.value)
    

