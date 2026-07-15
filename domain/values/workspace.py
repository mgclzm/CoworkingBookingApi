from dataclasses import dataclass
from datetime import time

from domain.entities.workspace import InvalidDescriptionError, InvalidNumberError, InvalidTitleError, InvalidWorkingTimeError

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
    

