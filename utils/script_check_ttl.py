from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import SecretModel
from core.database import get_session
import datetime


async def remove_secrets_by_ttl(
    db: AsyncSession = Depends(get_session),
):  # удаление секретов с истекшим сроком действия
    current_time = datetime.datetime.now(datetime.timezone.utc)
    query = db.query(SecretModel).filter(SecretModel.elapsed_at < current_time)
    await query.delete(synchronize_session=False)
