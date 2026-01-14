from fastapi import APIRouter, Request, HTTPException, Query
from asyncpg.exceptions import UniqueViolationError
from app.schemas import *
from app.queries import *
import bcrypt

router = APIRouter()

# User APIs
@router.post("/users", response_model=UserResponse)
async def create_user_f(payload: UserCreate, request: Request):
    try:
        hashed_pwd = bcrypt.hashpw(
            payload.password.encode(),
            bcrypt.gensalt()
        ).decode()

        return await create_user_q(
            request.app.state.pool,
            payload.username,
            hashed_pwd,
            payload.role
        )

    except UniqueViolationError:
        raise HTTPException(status_code=409, detail="Username exists")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    

# Issue APIs
@router.post("/issues", response_model=IssueResponse)
async def create_issue_f(payload: IssueCreate, request: Request):
    return await create_issue_q(
        request.app.state.pool,
        payload.title,
        payload.description,
        payload.priority
    )


@router.get("/issues", response_model=list[IssueResponse])
async def list_issues_f(
    request: Request,
    limit: int = Query(10, le=100),
    offset: int = 0
):
    return await list_issues_q(
        request.app.state.pool,
        limit,
        offset
    )


@router.get("/issues/{id}", response_model=IssueResponse)
async def get_issue_f(id: int, request: Request):
    issue = await get_issue_q(
        request.app.state.pool,
        id
    )
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.patch("/issues/{id}", response_model=IssueResponse)
async def update_issue_f(
    id: int,
    payload: IssueUpdate,
    request: Request
):
    issue = await update_issue_q(
        request.app.state.pool,
        id,
        payload.model_dump(exclude_unset=True)
    )

    if not issue:
        raise HTTPException(
            status_code=409,
            detail="Version conflict or issue not found"
        )

    return issue