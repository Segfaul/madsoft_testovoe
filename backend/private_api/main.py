import time
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from backend.public_api.config import ALLOWED_ORIGINS
from backend.private_api.router import upload_router
from backend.private_api.service.minio_service import get_minio_client

tags_metadata = [
    {
        "name": "Upload Meme",
        "description": "Upload endpoint",
    },
]


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    '''
    Asynchronous context manager to manage the lifespan of a FastAPI application's Minio connection.
    '''
    app_instance.state.minio_client = get_minio_client()
    if not app_instance.state.minio_client.bucket_exists('memes'):
        app_instance.state.minio_client.make_bucket('memes')
    try:
        yield
    finally:
        ...


app = FastAPI(
    title="Meme Private API",
    summary="Chilled api service for uploading memes 🐍",
    version='0.0.1',
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_url='/api/openapi.json',
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(upload_router, prefix="/api")


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    """
    TIMEOUT Middleware, throws an error if request exceeds 5s
    """
    start_time = time.time()
    try:
        return await asyncio.wait_for(call_next(request), timeout=5)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {
                'detail': 'Request processing time excedeed limit',
                'processing_time': process_time
            },
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )


@app.get("/api/swagger", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json", title="PrivateMemesAPI",
        swagger_favicon_url="https://i.postimg.cc/vm6NN3ms/meme-service.jpg"
    )


@app.get("/api/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/api/openapi.json", title="PrivateMemesAPI",
        redoc_favicon_url="https://i.postimg.cc/vm6NN3ms/meme-service.jpg"
    )
