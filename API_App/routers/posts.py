from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import oauth2
from ..database import get_db




router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[Schemas.GetRes])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all() #filter(models.Post.owner_id==get_current_user.id).
    return list(posts)


@router.post("/", response_model=Schemas.PostRes)
def create_posts(post: Schemas.CreatePost, db: Session = Depends(get_db),
                 get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=Schemas.GetRes)
def get_single_post(id: str, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posts not found with id {id}")
    return posts


@router.delete("/{id}")
def delete_posts(id: str, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"delete operation is not authorised for this owner {post.owner_id}")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}")
def patch_post(id: str, post: Schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists")
    if post_query.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"patch operation is not authorised for this owner {post.owner_id}")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"updated data": post_query.first()}
