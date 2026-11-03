from fastapi import FastAPI

from api.ideas.router import router as ideas_router


def create_app() -> FastAPI:
    app = FastAPI(title="Idea Management System")
    app.include_router(ideas_router)
    return app


app = create_app()
