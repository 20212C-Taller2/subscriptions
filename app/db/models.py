"""
Modelos para el ORM de la base de datos
"""

from sqlalchemy import Column, String, ForeignKey, Table, Integer, Numeric, DateTime, CheckConstraint
from sqlalchemy.orm import relationship

from .database import BaseModelDb

subscription_accesses = Table('subscription_accesses', BaseModelDb.metadata,
                              Column('subscription_parent_code',
                                     ForeignKey('subscription.code'),
                                     primary_key=True),
                              Column('subscription_accessed_code',
                                     ForeignKey('subscription.code'),
                                     primary_key=True)
                              )


class Subscription(BaseModelDb):
    __tablename__ = "subscription"

    code = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=21, scale=18), nullable=False)
    course_limit = Column(Integer, nullable=False)

    accesses = relationship(
        "Subscription",
        secondary=subscription_accesses,
        primaryjoin=code == subscription_accesses.c.subscription_parent_code,
        secondaryjoin=code == subscription_accesses.c.subscription_accessed_code)


class Course(BaseModelDb):
    __tablename__ = "course"

    course_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("subscriber.subscriber_id"), nullable=False)
    subscription_code = Column(String, ForeignKey("subscription.code"), nullable=False)
    subscription = relationship("Subscription")
    students = relationship("CourseStudent", cascade="all, delete", lazy="joined", back_populates="course")


class CourseStudent(BaseModelDb):
    __tablename__ = "course_student"
    __table_args__ = (
        CheckConstraint('payment_due_date > created_date', name='subscriber_suscription_payment_due_date_check'),
    )

    subscriber_id = Column(ForeignKey("subscriber.subscriber_id"), primary_key=True)
    subscriber = relationship("Subscriber")
    course_id = Column(ForeignKey("course.course_id"), primary_key=True)
    course = relationship("Course", back_populates="students")
    payment_status = Column(String,
                            nullable=False,
                            default="PENDING")
    price = Column(Numeric(precision=21, scale=18), nullable=False, default=0)
    created_date = Column(DateTime, nullable=False)
    payment_due_date = Column(DateTime, nullable=False)
    payment_collected_date = Column(DateTime, nullable=True)


class Subscriber(BaseModelDb):
    __tablename__ = "subscriber"

    subscriber_id = Column(String, primary_key=True, index=True)
    wallet_id = Column(String, nullable=False)
    address = Column(String, nullable=False)

    subscriptions = relationship("SubscriberSuscription", cascade="all, delete", lazy="joined")


class SubscriberSuscription(BaseModelDb):
    __tablename__ = "subscriber_suscription"

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(ForeignKey("subscriber.subscriber_id"), nullable=False)
    subscription_code = Column(ForeignKey("subscription.code"), nullable=False)
    created_date = Column(DateTime, nullable=False)
    courses_limit = Column(Integer, nullable=False)
    courses_used = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(precision=21, scale=18), nullable=False)
    subscription = relationship("Subscription")
