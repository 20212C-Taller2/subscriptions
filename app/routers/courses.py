from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.dependencies import get_db

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Course)
def create_course(course: schemas.Course, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course.course_id)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already registered")

    db_subscription = crud.get_subscription(db, subscription_code=course.subscription_code)
    if not db_subscription:
        raise HTTPException(status_code=400, detail="Invalid subscription")

    return crud.create_course(db=db, course=course)


@router.get("/{course_id}", response_model=schemas.Course)
def get_course(course_id: str, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404)

    return db_course
