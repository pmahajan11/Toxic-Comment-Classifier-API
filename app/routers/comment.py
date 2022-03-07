from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import models, oauth2, schemas
from app.database import get_db
from app.ml_main import preprocess, glove_dict, rfc_model


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get("/", response_model=List[schemas.CommentOut])
def get_comments(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = "", limit: int = 10, skip: int = 0):
    comments = db.query(models.Comment).filter(models.Comment.owner_id == current_user.id).filter(models.Comment.comment_text.contains(search)).limit(limit).offset(skip).all()
    return comments


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def evaluate_comment(comment: schemas.CommentBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_data = comment.dict()["comment_text"]
    toxic_score = round(rfc_model.predict_proba(preprocess(comment_data, glove_model=glove_dict))[0][1], 4)
    new_comment = models.Comment(owner_id=current_user.id, toxic_score=toxic_score, **comment.dict()) # unpack the post dictionary to fill the arguments
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{id}", response_model=schemas.CommentOut)
def get_comment(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("in get_comment")
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id {id} was not found")
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested acion!")
    return comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if comment.evaluator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested acion!")
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.CommentBase)
def update_comment(id: int, comment: schemas.CommentBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    if comment_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if comment_query.first().evaluator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested acion!")
    comment_query.update(comment.dict(), synchronize_session=False)
    db.commit()
    return comment_query.first()