import pytest

from app.ideas.models import Idea, IdeaStatus, InvalidStatusTransitionError


def test_cannot_approve_without_review():
    idea = Idea(title="X", description="", author_id="u1")
    with pytest.raises(InvalidStatusTransitionError):
        idea.approve()


def test_review_then_approve():
    idea = Idea(title="X", description="", author_id="u1")
    idea.start_review()
    idea.approve()
    assert idea.status is IdeaStatus.APPROVED
