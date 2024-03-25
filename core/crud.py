from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from utils.utils import generate_crypt_string
from core.models import SecretModel


async def add_in_db(secret, db):  # Создание объекта в БД
    db.add(secret)
    try:
        await db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            await db.rollback()
            secret.secret_key = generate_crypt_string()
            await add_in_db(secret)
    await db.refresh(secret)
    return secret


async def get_secret(secret_key, db):  # Получение объекта из БД
    secret = await db.execute(select(SecretModel).where(SecretModel.secret_key == secret_key))
    return secret.scalars().first()


async def delete_secret(secret, db):  # Удаление объекта из БД
    await db.delete(secret)
    await db.commit()
