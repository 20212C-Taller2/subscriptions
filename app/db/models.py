"""
Modelos para el ORM de la base de datos
"""

from sqlalchemy import Column, Integer, String
from app.db.database import BaseModelDb


class Subscription(BaseModelDb):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
