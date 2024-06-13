from io import BytesIO

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {
                "file": ("test_pic.jpg", BytesIO(b'meme content'), 'image/jpeg')
            },
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
    ),
)
async def test_upload_meme(
    client: AsyncClient,
    payload: dict, status_code: int
):
    response = await client.post("/meme/upload", files=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["file"][0] == response.json()["filename"]
