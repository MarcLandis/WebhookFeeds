import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from app.config import ASSETS_DIR
from app.database import create_db_and_tables
from app.routers import other, feeds, feeditems, feed_renderes, proxies


@asynccontextmanager
async def lifespan(_):
    create_db_and_tables()
    yield
    # Clean up


description = """
### A simple RESTful API to create and get feeds
[MIT license](./LICENSE.md)
"""

tags_metadata = [
    {
        "name": "feeds",
        "description": "Manage feeds.",
    },
    {
        "name": "feed items",
        "description": "Manage feed items.",
    },
    {
        "name": "feed renderer",
        "description": "Render feeds.",
    },
]

app = FastAPI(
    lifespan=lifespan,
    title="Webhook Feeds",
    version="0.1.0",
    description=description,
    redoc_url=None,
    docs_url=None,
)
app.include_router(other.router)
app.include_router(feeds.router)
app.include_router(feeditems.router)
app.include_router(feed_renderes.router)
app.include_router(proxies.router)

app.mount("/.assets", StaticFiles(directory=ASSETS_DIR), name=".assets")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
