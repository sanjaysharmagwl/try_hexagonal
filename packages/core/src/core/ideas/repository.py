from typing import Protocol
from uuid import UUID

from core.ideas.models import Idea


class IdeaRepository(Protocol):
    def save(self, idea: Idea) -> None: ...
    def get(self, idea_id: UUID) -> Idea | None: ...


class InMemoryIdeaRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, Idea] = {}

    def save(self, idea: Idea) -> None:
        self._store[idea.id] = idea

    def get(self, idea_id: UUID) -> Idea | None:
        return self._store.get(idea_id)
