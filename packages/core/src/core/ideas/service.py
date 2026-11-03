from core.ideas.models import Idea
from core.ideas.repository import IdeaRepository


class IdeaService:
    def __init__(self, ideas: IdeaRepository) -> None:
        self._ideas = ideas

    def submit(self, *, title: str, description: str, author_id: str) -> Idea:
        idea = Idea(title=title, description=description, author_id=author_id)
        self._ideas.save(idea)
        return idea
