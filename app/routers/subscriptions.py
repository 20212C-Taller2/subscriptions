from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.dependencies import get_db

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Subscription])
def get_subscriptions(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_db)):
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    return subscriptions
