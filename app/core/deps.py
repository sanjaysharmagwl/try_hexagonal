from fastapi import Request

from app.ideas.service import SubmitIdea


def get_submit_idea(request: Request) -> SubmitIdea:
    """Dependency function to get the SubmitIdea use case from app state."""
    return request.app.state.submit_idea
