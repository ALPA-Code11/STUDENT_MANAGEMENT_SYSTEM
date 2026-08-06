from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# .env file load karein
load_dotenv()

# Apne saare models aur Base import karein taaki alembic ko tables ka pata chale
from database import Base
from app.models.user_model import User
from app.models.role_model import role_model
from app.models.permission_model import permission_model
from app.models.role_permission_model import role_permission_model
from app.models.refresh_token_model import RefreshToken

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata yahan link kiya gaya hai
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # .env se direct URL yahan bhi utha liya
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # .env se URL uthakar alembic ki configuration mein set karna
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()