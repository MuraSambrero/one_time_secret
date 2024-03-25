from fastapi import FastAPI
from routers.router_index import router

app = FastAPI()

app.include_router(router=router, prefix="/api")
