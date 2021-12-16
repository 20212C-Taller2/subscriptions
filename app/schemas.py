"""
Estos son los "modelos" de pydantic que son usados por la api para validar
campos
"""
import decimal
from typing import List

from pydantic import BaseModel


class Subscription(BaseModel):
    code: str
    description: str
    # accesses: List['Subscription'] = []
    price: decimal.Decimal
    course_limit: int

    class Config:
        orm_mode = True


Subscription.update_forward_refs()


class Course(BaseModel):
    course_id: str
    owner_id: str
    subscription_code: str

    class Config:
        orm_mode = True


class SubscriberSubscriptionCreate(BaseModel):
    subscription_code: str

    class Config:
        orm_mode = True


class SubscriberSubscription(SubscriberSubscriptionCreate):
    courses_limit: int
    courses_used: int

    class Config:
        orm_mode = True


class SubscriberCreate(BaseModel):
    subscriber_id: str

    class Config:
        orm_mode = True


class SubscriberReturn(SubscriberCreate):
    address: str
    balance: decimal.Decimal = 0
    subscriptions: List[SubscriberSubscription] = []

    class Config:
        orm_mode = True


class Subscriber(SubscriberReturn):
    wallet_id: str

    class Config:
        orm_mode = True
