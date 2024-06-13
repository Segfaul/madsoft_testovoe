from typing import Optional

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    (
        (
            {
                "title": "dude",
                "image_url": "http://localhost:9000/random.jpeg"
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                "title": "newbie",
                "image_url": "http://localhost:9000/random.txt"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "title": "dude",
                "image_url": "http://localhost:9000/random.jpeg"
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ),
)
async def test_add_meme(
    client: AsyncClient,
    payload: dict, status_code: int
):
    response = await client.post("/meme/", json=payload)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert payload["title"] == response.json()["title"]


@pytest.mark.parametrize(
    "meme_id, params, status_code",
    (
        (
            None,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
    ),
)
async def test_get_meme(
    client: AsyncClient,
    meme_id: Optional[int], params: dict, status_code: int
):
    response = await client.get(f"/meme/{meme_id if meme_id else ''}", params=params)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "meme_id, payload, status_code",
    (
        (
            1,
            {},
            status.HTTP_200_OK,
        ),
        (
            1,
            {
                "description": "some funny dude..."
            },
            status.HTTP_200_OK,
        ),
        (
            2,
            {},
            status.HTTP_404_NOT_FOUND,
        ),
    ),
)
async def test_upd_meme(
    client: AsyncClient,
    meme_id: Optional[int], payload: dict, status_code: int
):
    response = await client.patch(f"/meme/{meme_id}", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "meme_id, status_code",
    (
        (
            1,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            2,
            status.HTTP_404_NOT_FOUND,
        )
    ),
)
async def test_delete_meme(
    client: AsyncClient,
    meme_id: Optional[int], status_code: int
):
    response = await client.delete(f"/meme/{meme_id}")
    assert response.status_code == status_code
