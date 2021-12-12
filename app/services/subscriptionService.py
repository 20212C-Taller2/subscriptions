import itertools

from .. import schemas


def group_subscriptions(subscriber: schemas.Subscriber) -> schemas.Subscriber:
    """
    Simplifies subscriptions list returned one grouped subscription code with the totals courses limits
    """
    def order_func(x):
        return x.subscription_code

    subscriptions = []
    subs = sorted(subscriber.subscriptions, key=order_func)

    for key, value in itertools.groupby(subs, key=order_func):
        subscriptions.append(
            {
                "subscription_code": key,
                "courses_limit": sum([x.courses_limit for x in value]),
                "courses_used": sum([x.courses_used for x in value])
            }
        )

    return_subscriber = subscriber.dict()
    return_subscriber["subscriptions"] = subscriptions
    return schemas.Subscriber(**return_subscriber)
