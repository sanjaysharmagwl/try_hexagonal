import pytest
from core.ideas.models import DomainError, IdeaStatus
from core.ideas.repository import InMemoryIdeaRepository
from core.ideas.service import IdeaService


def test_submit_stores_and_returns_idea():
    """Requirement: Idea Submission / Idea Initial State."""
    repo = InMemoryIdeaRepository()
    service = IdeaService(repo)

    idea = service.submit(title="Dark mode", description="Add a theme", author_id="u1")

    assert idea.status is IdeaStatus.SUBMITTED
    assert repo.get(idea.id) is idea


def test_submit_whitespace_title_raises_domain_error():
    """Requirement: Idea Submission — blank title rejected by domain."""
    service = IdeaService(InMemoryIdeaRepository())

    # EmptyTitleError (a DomainError) propagates out of Idea's pydantic
    # field_validator unwrapped — pydantic only wraps ValueError/AssertionError.
    with pytest.raises(DomainError, match="cannot be empty"):
        service.submit(title="   ", description="", author_id="u1")
