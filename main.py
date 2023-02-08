import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.database import engine
from user import models, routers as user_routers
from rate import routers as rate_routers
from services import routers as service_routers
from user_bought_service import routers as connected_service_routers

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers.router, tags=['User'], prefix='/api')
app.include_router(rate_routers.router, tags=['Rate'], prefix='/api')
app.include_router(service_routers.router, tags=['Services'], prefix='/api')
app.include_router(connected_service_routers.router, tags=['Connected services'], prefix='/api')


@app.on_event("startup")
async def startup_event():
    # models.Base.metadata.create_all(bind=engine)
    async with engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)