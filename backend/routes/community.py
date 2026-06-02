import uuid
import time
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Query
from typing import Dict, Any, List, Optional
from models.community import PostResponse, CommentResponse
from database.firebase import db_client, storage_bucket
from app.dependencies import get_current_user
from app.exceptions import NotFoundException, PermissionDeniedException, TerravaException

router = APIRouter(prefix="/community", tags=["Community Social Platform"])


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None, description="Attach optional photo to post"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    post_id = str(uuid.uuid4())
    
    # Retrieve grower info
    user_snap = db_client.collection("users").document(uid).get()
    author_name = user_snap.to_dict().get("name", "Unknown Farmer") if user_snap.exists else "Unknown Farmer"

    # Ingest attached media
    image_url = None
    if image:
        if not image.content_type.startswith("image/"):
            raise TerravaException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported media format")
        
        try:
            content_bytes = await image.read()
            blob_path = f"community_posts/{post_id}.jpg"
            blob = storage_bucket.blob(blob_path)
            blob.upload_from_string(content_bytes, content_type="image/jpeg")
            image_url = blob.generate_signed_url(expiration=31536000)  # 1 year
        except Exception:
            image_url = f"https://terrava-farm.web.app/assets/posts/{post_id}.jpg"

    post_data = {
        "post_id": post_id,
        "author_uid": uid,
        "author_name": author_name,
        "title": title,
        "content": content,
        "image_url": image_url,
        "likes": [],
        "comments": [],
        "created_at": float(time.time())
    }

    db_client.collection("community_posts").document(post_id).set(post_data)
    
    return PostResponse(
        post_id=post_id,
        author_uid=uid,
        author_name=author_name,
        title=title,
        content=content,
        image_url=image_url,
        likes=[],
        comments=[],
        created_at=time.time()
    )


@router.get("/posts", response_model=List[PostResponse])
async def list_posts(current_user: Dict[str, Any] = Depends(get_current_user)):
    posts_docs = db_client.collection("community_posts").get()
    
    posts_list = []
    for doc in posts_docs:
        data = doc.to_dict()
        posts_list.append(PostResponse(**data))
        
    # Sort posts chronologically (latest first)
    return sorted(posts_list, key=lambda x: x.created_at, reverse=True)


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    post_ref = db_client.collection("community_posts").document(post_id)
    post_snap = post_ref.get()
    
    if not post_snap.exists:
        raise NotFoundException("Post not found")
        
    post_data = post_snap.to_dict()
    
    # Restrict deletions to author or admins
    if post_data["author_uid"] != uid and current_user["role"] != "admin":
        raise PermissionDeniedException("You are not authorized to delete this post")
        
    post_ref.delete()
    return {"message": "Post successfully deleted"}


@router.post("/posts/{post_id}/like", response_model=PostResponse)
async def like_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    post_ref = db_client.collection("community_posts").document(post_id)
    post_snap = post_ref.get()
    
    if not post_snap.exists:
        raise NotFoundException("Post not found to process like")
        
    post_data = post_snap.to_dict()
    likes = post_data.get("likes", [])
    
    if uid in likes:
        likes.remove(uid)  # Unlike if already liked
    else:
        likes.append(uid)  # Like
        
    post_ref.update({"likes": likes})
    post_data["likes"] = likes
    
    return PostResponse(**post_data)


@router.post("/posts/{post_id}/comments", response_model=PostResponse)
async def comment_on_post(
    post_id: str,
    content: str = Form(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    post_ref = db_client.collection("community_posts").document(post_id)
    post_snap = post_ref.get()
    
    if not post_snap.exists:
        raise NotFoundException("Post not found to add comment")
        
    post_data = post_snap.to_dict()
    comments = post_data.get("comments", [])
    
    # Retrieve commenter info
    user_snap = db_client.collection("users").document(uid).get()
    author_name = user_snap.to_dict().get("name", "Unknown Farmer") if user_snap.exists else "Unknown Farmer"

    comment_id = str(uuid.uuid4())
    comment_data = {
        "comment_id": comment_id,
        "post_id": post_id,
        "author_uid": uid,
        "author_name": author_name,
        "content": content,
        "created_at": float(time.time())
    }
    
    comments.append(comment_data)
    post_ref.update({"comments": comments})
    post_data["comments"] = comments
    
    return PostResponse(**post_data)
