from datetime import time

from pydantic import BaseModel

class RegisterWorkspaceRequestSchema(BaseModel):
    opening_time: time
    closing_time: time
    location: str
    description: str


class RegisterWorkspaceResponseSchema(BaseModel):
    workspace_id: str
    owner_id: str
    opening_time: time
    closing_time: time
    location: str
    description: str
    