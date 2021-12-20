import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.dependencies import get_db
from app.services import subscriptionService

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


@router.post("/{course_id}/subscribeStudent", response_model=schemas.Course)
def create_course_subscription(course_id: str,
                               student_subscription: schemas.SubscribeStudent,
                               db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course Not Found")

    db_subscriber = crud.get_subscriber(db, subscriber_id=student_subscription.subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404, detail="SubscriberNotFound")

    db_sub_subs = subscriptionService.get_subscription_to_consume(db, db_subscriber, db_course.subscription)
    if not db_sub_subs:
        raise HTTPException(status_code=404, detail="No active subscription")

    db_student = crud.get_student(db, db_subscriber, db_course)
    if db_student:
        raise HTTPException(status_code=422, detail="Student already enrolled")

    return crud.create_course_student(db, db_course, db_subscriber, db_sub_subs)


@router.delete("/{course_id}/subscribeStudent/{subscriber_id}")
def delete_course_subscription(course_id: str,
                               subscriber_id: str,
                               db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course Not Found")

    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404, detail="SubscriberNotFound")

    db_student = crud.get_student(db, db_subscriber, db_course)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    if db_student.payment_due_date <= datetime.datetime.now():
        raise HTTPException(status_code=422, detail="Remorse time passed")

    return crud.delete_course_student(db, db_student)
