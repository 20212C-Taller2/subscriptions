"""
Modelos para el ORM de la base de datos
"""

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.database import BaseModelDb

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

    accesses = relationship(
        "Subscription",
        secondary=subscription_accesses,
        primaryjoin=code == subscription_accesses.c.subscription_parent_code,
        secondaryjoin=code == subscription_accesses.c.subscription_accessed_code)


class Course(BaseModelDb):
    __tablename__ = "course"

    course_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, nullable=False)
    subscription_code = Column(String, ForeignKey("subscription.code"), nullable=False)
    subscription = relationship("Subscription")
