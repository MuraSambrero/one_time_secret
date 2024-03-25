from fastapi.routing import APIRouter
from .router_api import router_api

router = APIRouter()

router.include_router(router_api)
