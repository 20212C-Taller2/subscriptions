"""
Estos son los "modelos" de pydantic que son usados por la api para validar
campos
"""


from pydantic import BaseModel


class Subscription(BaseModel):
    code: str
    description: str
    # accesses: List['Subscription'] = []

    class Config:
        orm_mode = True


Subscription.update_forward_refs()
