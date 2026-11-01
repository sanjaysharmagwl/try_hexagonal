from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class DomainError(Exception):
    """Base class for business rule violations."""


class EmptyTitleError(DomainError):
    pass


class InvalidStatusTransitionError(DomainError):
    pass


class IdeaStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class Idea(BaseModel):
    title: str
    description: str
    author_id: str
    id: UUID = Field(default_factory=uuid4)
    status: IdeaStatus = IdeaStatus.SUBMITTED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise EmptyTitleError("Idea title cannot be empty")
        return v.strip()

    def start_review(self) -> None:
        if self.status is not IdeaStatus.SUBMITTED:
            raise InvalidStatusTransitionError(
                f"Cannot start review from status '{self.status.value}'"
            )
        self.status = IdeaStatus.UNDER_REVIEW

    def approve(self) -> None:
        if self.status is not IdeaStatus.UNDER_REVIEW:
            raise InvalidStatusTransitionError(
                f"Cannot approve idea in status '{self.status.value}'"
            )
        self.status = IdeaStatus.APPROVED
