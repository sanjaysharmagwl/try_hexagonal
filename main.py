from fastapi import FastAPI

from app.ideas.repository import InMemoryIdeaRepository
from app.ideas.router import router
from app.ideas.service import SubmitIdea


def create_app() -> FastAPI:
    app = FastAPI(title="Idea Management System")

    # Wire adapters to use cases in one place
    repository = InMemoryIdeaRepository()
    app.state.submit_idea = SubmitIdea(ideas=repository)

    app.include_router(router)
    return app


app = create_app()
