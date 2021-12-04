from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.dependencies import get_db
from ..services import walletService

router = APIRouter(
    prefix="/subscribers",
    tags=["subscribers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Subscriber)
def create_subscriber(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber.subscriber_id)
    if db_subscriber:
        raise HTTPException(status_code=400, detail="Subscriber already registered")

    sub = schemas.Subscriber(**subscriber.dict(), wallet_id=walletService.create_wallet())

    return crud.create_subscriber(db=db, subscriber=sub)


@router.get("/{subscriber_id}", response_model=schemas.Subscriber)
def get_subscriber(subscriber_id: str, db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404)

    return db_subscriber
