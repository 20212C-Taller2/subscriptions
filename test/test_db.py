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
    def get_url():
        if os.environ.get("DATABASE_URL") is not None:
            uri = os.getenv("DATABASE_URL")  # or other relevant config var
            if uri and uri.startswith("postgres://"):
                uri = uri.replace("postgres://", "postgresql://", 1)
                return uri
        return os.environ["FASTAPI_POSTGRESQL"]

    SQLALCHEMY_DATABASE_URL = get_url()

    e = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    cfg = config.Config("alembic.ini")
    assert check_current_head(cfg, e)
