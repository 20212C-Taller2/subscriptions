"""
Estos son los "modelos" de pydantic que son usados por la api para validar
campos
"""

from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    code: str
    description: str


class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True
