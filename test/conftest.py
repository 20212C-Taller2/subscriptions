import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import schemas
from app.db import crud
from app.db.database import BaseModelDb
from app.db.models import Subscription
from app.dependencies import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = os.environ["TEST_FASTAPI_POSTGRESQL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    BaseModelDb.metadata.drop_all(bind=engine)
    BaseModelDb.metadata.create_all(bind=engine)

    app.dependency_overrides = {}

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


@pytest.fixture
def subscriber():
    db = TestingSessionLocal()
    s = crud.create_subscriber(db, schemas.Subscriber(subscriber_id="1", address="fakeaddr", wallet_id="fakeprivkey"))
    sub = schemas.Subscriber(**s.__dict__)
    db.close()
    return sub


@pytest.fixture
def basic_subscription():
    expected_subscriptions = {"code": "BASIC", "description": "Basic Subscription", "price": 1e-06, "course_limit": 5}

    db = TestingSessionLocal()

    s = Subscription(**expected_subscriptions)
    db.add(s)
    db.commit()
    db.refresh(s)
    db.close()
    return schemas.Subscription(**s.__dict__)
