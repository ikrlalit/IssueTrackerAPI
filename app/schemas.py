from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserResponse(BaseModel):
    useruuid: UUID
    username: str
    role: str
    created_at: datetime


class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None

class IssueUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]

class IssueResponse(BaseModel):
    issueuuid: UUID
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    version: int
    created_at: datetime


class CommentCreate(BaseModel):
    content: str
    user_id: int

class LabelReplace(BaseModel):
    label_ids: List[int]

class BulkStatusUpdate(BaseModel):
    issue_ids: List[int]
    status: str