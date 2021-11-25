import os

from alembic import config, script
from alembic.runtime import migration
from sqlalchemy import engine, create_engine


def check_current_head(alembic_cfg, connectable):
    # type: (config.Config, engine.Engine) -> bool
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


def test_db():
    SQLALCHEMY_DATABASE_URL = os.environ['FASTAPI_POSTGRESQL']

    e = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    cfg = config.Config("alembic.ini")
    assert check_current_head(cfg, e)
