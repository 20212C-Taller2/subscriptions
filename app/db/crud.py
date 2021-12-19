from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import models
from .. import schemas, constants


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()


def get_subscription(db: Session, subscription_code: str):
    return db.query(models.Subscription).get(subscription_code)


def create_course(db: Session, course: schemas.Course):
    subscription = db.query(models.Subscription).get(course.subscription_code)
    db_course = models.Course(
        course_id=course.course_id,
        owner_id=course.owner_id,
        subscription=subscription)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_course(db: Session, course_id: str):
    return db.query(models.Course).get(course_id)


def create_subscriber(db: Session, subscriber: schemas.Subscriber):
    db_subscriber = models.Subscriber(subscriber_id=subscriber.subscriber_id,
                                      wallet_id=subscriber.wallet_id,
                                      address=subscriber.address)
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


def get_subscriber(db: Session, subscriber_id: str):
    return db.query(models.Subscriber).get(subscriber_id)


def add_subscription(db: Session, subscriber: models.Subscriber, subscription: models.Subscription):
    created_Date = datetime.now()
    db_subscriber_subscription = models.SubscriberSuscription(created_date=datetime.now(),
                                                              courses_limit=subscription.course_limit,
                                                              price=subscription.price,
                                                              payment_status=constants.PaymentStatus.PAYMENT_PENDING,
                                                              payment_due_date=created_Date + timedelta(
                                                                  days=constants.DAYS_TO_REMORSE))
    db_subscriber_subscription.subscription = subscription
    subscriber.subscriptions.append(db_subscriber_subscription)
    db.commit()
    db.refresh(subscriber)
    return subscriber
