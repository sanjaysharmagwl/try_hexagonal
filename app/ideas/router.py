from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_submit_idea
from app.ideas.models import DomainError
from app.ideas.schemas import IdeaResponse, SubmitIdeaRequest
from app.ideas.service import SubmitIdea, SubmitIdeaCommand

router = APIRouter(prefix="/ideas", tags=["ideas"])


@router.post("", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def submit_idea(
    body: SubmitIdeaRequest,
    use_case: SubmitIdea = Depends(get_submit_idea),
) -> IdeaResponse:
    try:
        idea = use_case.execute(
            SubmitIdeaCommand(
                title=body.title,
                description=body.description,
                author_id=body.author_id,
            )
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
