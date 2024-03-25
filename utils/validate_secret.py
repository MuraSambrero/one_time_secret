from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from core.models import SecretModel
from schemas.schema_app import SecretResponse
from cryptography.fernet import InvalidToken
from core.crud import delete_secret
from utils.crypt import decrypt_message


async def secret_validation(secret: SecretModel, item: SecretResponse, db: AsyncSession) -> str:
    if secret is None: # Если секрета с таким ключем нет
        return "Секрет истек, либо данного ключа не существует."
    if (
        datetime.datetime.now(datetime.timezone.utc) > secret.elapsed_at
    ):  # проверка истечения срока действия секрета по запрашиваемому ключу
        await delete_secret(secret, db)
        return "Секрет истек."
    try:
        decrypted = decrypt_message(
            secret.secret_data, item.code_phrase
        )  # дешифрование данных секрета
    except InvalidToken:
        return "Неверная кодовая фраза."
    await delete_secret(secret, db)
    return decrypted