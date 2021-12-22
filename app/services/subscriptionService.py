import itertools

from sqlalchemy.orm import Session

from .. import schemas
from ..db import models


def group_subscriptions(subscriber: schemas.SubscriberReturn) -> schemas.SubscriberReturn:
    """
    Simplifies subscriptions list returned one grouped subscription code with the totals courses limits
    """

    def order_func(x):
        return x.subscription_code

    subscriptions = []
    subs = sorted(subscriber.subscriptions, key=order_func)

    for key, value in itertools.groupby(subs, key=order_func):
        c_limit = 0
        c_used = 0
        for x in value:
            c_limit += x.courses_limit
            c_used += x.courses_used
        subscriptions.append(
            {
                "subscription_code": key,
                "courses_limit": c_limit,
                "courses_used": c_used
            }
        )

    return_subscriber = subscriber.dict()
    return_subscriber["subscriptions"] = subscriptions
    return schemas.SubscriberReturn(**return_subscriber)


def get_subscription_to_consume(db: Session,
                                subscriber: models.Subscriber,
                                course_subscription: models.Subscription) -> models.SubscriberSuscription:
    access = None
    if course_subscription.code == "FULL":
        access = ("FULL",)
    elif course_subscription.code == "BASIC":
        access = ("BASIC", "FULL")
    else:
        raise ValueError("Not implemented subscription code")

    return db.query(models.SubscriberSuscription).filter(
        models.SubscriberSuscription.subscriber_id == subscriber.subscriber_id,
        models.SubscriberSuscription.courses_limit > models.SubscriberSuscription.courses_used,
        models.SubscriberSuscription.subscription_code.in_(access)
    ).order_by(models.SubscriberSuscription.created_date).with_for_update().first()
