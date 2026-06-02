from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class CommentResponse(BaseModel):
    comment_id: str
    post_id: str
    author_uid: str
    author_name: str
    content: str
    created_at: datetime


class PostCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    content: str = Field(..., min_length=5, max_length=5000)
    image_url: Optional[str] = None


class PostResponse(BaseModel):
    post_id: str
    author_uid: str
    author_name: str
    title: str
    content: str
    image_url: Optional[str] = None
    likes: List[str] = []  # List of UIDs of users who liked this post
    comments: List[CommentResponse] = []
    created_at: datetime
