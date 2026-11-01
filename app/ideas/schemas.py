from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SubmitIdeaRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    author_id: str


class IdeaResponse(BaseModel):
    id: UUID
    title: str
    description: str
    author_id: str
    status: str
    created_at: datetime
