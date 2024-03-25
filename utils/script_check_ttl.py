from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import SecretModel
from core.crud import delete_secret
from core.database import get_session
import datetime


async def remove_secrets_by_ttl(
    db: AsyncSession = Depends(get_session),
):  # удаление секретов с истекшим сроком действия
    current_time = datetime.datetime.now(datetime.timezone.utc)
    secrets: list[SecretModel] = await db.execute(
        select(SecretModel).where(
            SecretModel.elapsed_at < current_time
        )
    )
    for secret in secrets.scalars().all():
        if (
            datetime.datetime.now(datetime.timezone.utc) > secret.elapsed_at
        ):  # проверка истечения срока действия секрета
            await delete_secret(secret, db)
