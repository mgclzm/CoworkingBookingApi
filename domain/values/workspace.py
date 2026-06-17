from dataclasses import dataclass, field
from datetime import time

from domain.exceptions.errors import InvalidSpotTitleError, InvalidSpotNumberError, InvalidWorkingTimeError, InvalidDescriptionError

@dataclass(frozen=True)
class SpotTitle:
    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise InvalidSpotTitleError('Title cannot be empty')

@dataclass(frozen=True)
class SpotNumber:
    value: int

    def __post_init__(self):
        if self.value <= 0 or self.value > 100:
            raise InvalidSpotNumberError(f'Spot number must be between 1 and 100, got {self.value}')
        
@dataclass(frozen=True)
class WorkingTime:
    opening_time: time
    closing_time: time

    def __post_init__(self):
        if self.opening_time >= self.closing_time:
            raise InvalidWorkingTimeError('Opening time must be before closing time')
        
@dataclass(frozen=True)
class WorkspaceDescription: 
    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise InvalidDescriptionError(f'Workspace description must me less then 1000, actual length {len(self.value)}')
    

