from functools import lru_cache

from core.ideas.repository import IdeaRepository, InMemoryIdeaRepository
from core.ideas.service import IdeaService
from fastapi import Depends


@lru_cache
def get_idea_repository() -> IdeaRepository:
    return InMemoryIdeaRepository()


def get_idea_service(repo: IdeaRepository = Depends(get_idea_repository)) -> IdeaService:
    return IdeaService(repo)
