import uvicorn

from api.routes import router as api_router
from core.config import settings
from fastapi import FastAPI


app = FastAPI()
app.include_router(
    router=api_router,
    prefix=settings.api.prefix,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.run.host, port=settings.run.port, reload=True)
