from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils.utils import generate_crypt_string
from utils.crypt import encrypt_message
from schemas.schema_app import Secret, SecretResponse
from core.models import SecretModel
from core.crud import add_in_db
from core.crud import get_secret
from core.database import get_session
from utils.utils import time_to_end
from utils.validate_secret import secret_validation
from utils.script_check_ttl import remove_secrets_by_ttl


async def create_secret(
    item: Secret,
    db: AsyncSession = Depends(get_session),
) -> str:  # получение уникального ключа и создание секрета в БД
    secret_key = generate_crypt_string()  # генерация уникального ключа
    encrypted = encrypt_message(
        item.secret_data, item.code_phrase
    )  # шифрование данных секрета
    secret = SecretModel(
        secret_data=encrypted,
        secret_key=secret_key,
        elapsed_at=time_to_end(item.ttl),
    )
    create_obj = await add_in_db(secret, db)
    return create_obj.secret_key


async def get_secret_by_key(
    item: SecretResponse,
    secret_key: str,
    db: AsyncSession = Depends(get_session),
) -> SecretModel:  # получение данных секрета по ключу
    await remove_secrets_by_ttl(db)  # удаление секретов, с истекшим сроком действия
    secret: SecretModel = await get_secret(secret_key, db)  # получение секрета по ключу
    answer_validate = await secret_validation(
        secret, item, db
    )  # проверка секрета на истечение срока действия
    return answer_validate
