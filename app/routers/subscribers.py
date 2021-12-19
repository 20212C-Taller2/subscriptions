from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import crud
from app.dependencies import get_db
from ..constants import EthTxProcessResult
from ..schemas import SubscriberReturn
from ..services import walletService, subscriptionService

router = APIRouter(
    prefix="/subscribers",
    tags=["subscribers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

wallet_service = walletService.WalletService()


@router.post("/", response_model=schemas.SubscriberReturn)
def create_subscriber(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber.subscriber_id)
    if db_subscriber:
        raise HTTPException(status_code=400, detail="Subscriber already registered")

    wallet = wallet_service.create_wallet()
    sub = schemas.Subscriber(**subscriber.dict(),
                             wallet_id=wallet['private_key'],
                             address=wallet['address'])

    return crud.create_subscriber(db=db, subscriber=sub)


@router.get("/{subscriber_id}", response_model=schemas.SubscriberReturn)
def get_subscriber(subscriber_id: str, db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404)

    subscriber_schema = SubscriberReturn(**db_subscriber.__dict__)
    subscriber_schema.balance = wallet_service.get_balance(subscriber_schema.address)
    return subscriptionService.group_subscriptions(subscriber_schema)


@router.post("/{subscriber_id}/subscription", response_model=schemas.SubscriberReturn)
def add_subscription(subscriber_id: str,
                     subscription: schemas.SubscriberSubscriptionCreate,
                     db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id=subscriber_id)
    if not db_subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    db_subscription = crud.get_subscription(db, subscription_code=subscription.subscription_code)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    try:
        deposit_result = wallet_service.deposit(db_subscriber.address,
                                                db_subscriber.wallet_id,
                                                db_subscription.price)
        if deposit_result == EthTxProcessResult.ERROR:
            raise HTTPException(status_code=422, detail="Unable to process payment")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing payment: {e}")

    crud.add_subscription(db, db_subscriber, db_subscription)
    db.refresh(db_subscriber)
    subscriber_return = schemas.SubscriberReturn(**db_subscriber.__dict__)
    subscriber_return.balance = wallet_service.get_balance(subscriber_return.address)
    return subscriptionService.group_subscriptions(subscriber_return)
