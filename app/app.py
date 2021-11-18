from fastapi import FastAPI

from app import config
from app.api.exceptions.handlers import exception_handlers
from app.api.v1.router import api_v1_router

__version__ = "0.0.1"

# Setup app
app = FastAPI(
    debug=config.APP_DEBUG,
    title=config.APP_TITLE,
    openapi_url=config.APP_OPENAPI_URL,
    version=__version__,
    exception_handlers=exception_handlers,
)

app.include_router(api_v1_router, prefix=config.APP_API_V1_PREFIX)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.app:app", host="0.0.0.0", port=80, reload=True)
