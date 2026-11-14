from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Проекттин база дарегин жана моделдерин импорттойбуз
from mysite.database.db import Base, SQLALCHEMY_DATABASE_URL
from mysite.database.models import User, Category, Store, Product, Review, City, Order

config = context.config

# Базанын URL дарегин мажбурлап бекитебиз (driver катасы чыкпашы үчүн)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ЭҢ МААНИЛҮҮСҮ: Alembic таануучу MetaData объекти
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"server_side_only": True},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata  # <-- Бул жер сөзсүз болушу керек!
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_active:
    run_migrations_offline()
else:
    run_migrations_online()