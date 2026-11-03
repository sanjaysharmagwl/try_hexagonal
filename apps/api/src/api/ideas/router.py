from core.ideas.models import DomainError
from core.ideas.service import IdeaService
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_idea_service
from api.ideas.schemas import IdeaResponse, SubmitIdeaRequest

router = APIRouter(prefix="/ideas", tags=["ideas"])


@router.post("", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def submit_idea(
    body: SubmitIdeaRequest,
    service: IdeaService = Depends(get_idea_service),
) -> IdeaResponse:
    try:
        idea = service.submit(
            title=body.title,
            description=body.description,
            author_id=body.author_id,
        )
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    return IdeaResponse(
        id=idea.id,
        title=idea.title,
        description=idea.description,
        author_id=idea.author_id,
        status=idea.status.value,
        created_at=idea.created_at,
    )
