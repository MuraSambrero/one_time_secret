from fastapi import Depends
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import APIRouter
from schemas.schema_app import Secret, SecretResponse
from views.view import create_secret, get_secret_by_key
#from core.database import get_db
from core.database import get_session


router_api = APIRouter()


@router_api.post("/generate")
async def generate(item: Secret, db: AsyncSession = Depends(get_session)):
    secret_key = await create_secret(item, db)
    return secret_key


@router_api.post("/secrets/{secret_key}")
async def get_secret(
    item: SecretResponse,
    secret_key: str,
    db: AsyncSession = Depends(get_session),
):
    secret = await get_secret_by_key(item, secret_key, db)
    return secret
