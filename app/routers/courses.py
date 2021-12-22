import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import schemas, constants
from app.db import crud
from app.db.models import CourseStudent
from app.dependencies import get_db
from app.services import subscriptionService
from app.services.walletService import WalletService

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

_walletService = WalletService()


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

    db_sub_subs = subscriptionService.get_subscription_to_consume(db, db_subscriber, db_course.basic_subscription)
    if not db_sub_subs:
        raise HTTPException(status_code=404, detail="No active subscription")

    db_student = crud.get_student(db, db_subscriber, db_course)
    if db_student:
        raise HTTPException(status_code=422, detail="Student already enrolled")

    return crud.create_course_student(db, db_course, db_subscriber, db_sub_subs)


@router.post("/processPayments")
async def process_payments(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(do_process_payments, db)
    return {"message": "Payment process started"}


def do_process_payments(db):
    logging.info("Payment Process Started")
    now = datetime.datetime.now()
    payments_to_process = db.query(CourseStudent).filter(
        CourseStudent.payment_due_date <= now,
        CourseStudent.payment_status == constants.PaymentStatus.PAYMENT_PENDING).with_for_update().all()
    for payment in payments_to_process:
        try:
            res = _walletService.send_payment(payment.subscriber.address, payment.price)
            if res == constants.EthTxProcessResult.OK:
                payment.payment_status = constants.PaymentStatus.PAYMENT_ACCEPTED
                payment.payment_collected_date = datetime.datetime.now()
            else:
                logging.error(f"Failed to process payment for course {payment.course_id} and subscriber "
                              f"{payment.subscriber_id}")
        except Exception as e:
            logging.error(f"Unable to process payment for course {payment.course_id} and subscriber "
                          f"{payment.subscriber_id} with error {e}")
    logging.info(f"Payment Process Finished: {len(payments_to_process)} records processed")
    db.commit()


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
