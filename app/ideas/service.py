from pydantic import BaseModel

from app.ideas.models import Idea
from app.ideas.repository import IdeaRepository


class SubmitIdeaCommand(BaseModel):
    title: str
    description: str
    author_id: str


class SubmitIdea:
    def __init__(self, ideas: IdeaRepository) -> None:
        self._ideas = ideas

    def execute(self, command: SubmitIdeaCommand) -> Idea:
        idea = Idea(
            title=command.title,
            description=command.description,
            author_id=command.author_id,
        )
        self._ideas.save(idea)
        return idea
