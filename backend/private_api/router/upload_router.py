from io import BytesIO

from fastapi import APIRouter, HTTPException, UploadFile, File, status, Request
from minio.error import S3Error

from backend.private_api.schema import UploadMemeResponse, MemeURLsResponse
from backend.private_api.service.minio_service import MINIO_URL

ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/bmp", "image/webp", "image/tiff"}

router = APIRouter(
    prefix="/v1/meme",
    tags=['Upload Meme']
)

@router.get(
    "/urls", status_code=status.HTTP_200_OK,
    response_model=MemeURLsResponse, response_model_exclude_unset=True
)
async def read_all_meme_urls(
    request: Request
):
    try:
        minio_client = request.app.state.minio_client
        objects = minio_client.list_objects(bucket_name='memes', recursive=True)
        meme_urls = [f"{MINIO_URL}/memes/{obj.object_name}" for obj in objects]
        return MemeURLsResponse(urls=meme_urls).model_dump(exclude_unset=True)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post(
    "/upload", status_code=status.HTTP_201_CREATED,
    response_model=UploadMemeResponse, response_model_exclude_unset=True
)
async def upload_meme(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only jpg/jpeg/png/gif/bmp/webp/tiff files are allowed."
            )
        content = await file.read()
        file_stream = BytesIO(content)
        minio_client = request.app.state.minio_client
        minio_client.put_object(
            bucket_name='memes',
            object_name=file.filename,
            data=file_stream,
            length=len(content),
            content_type=file.content_type
        )
        return UploadMemeResponse(
            filename=file.filename,
            url=f"{MINIO_URL}/memes/{file.filename}"
        ).model_dump(exclude_unset=True)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
