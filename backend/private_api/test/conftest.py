# pylint: disable=C0413,C0114
import pytest
from httpx import AsyncClient, ASGITransport

from backend.public_api.main import app

@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request):
    return request.param

@pytest.fixture(scope="session", autouse=True)
async def client() -> AsyncClient:
    transport = ASGITransport(
        app=app,
    )
    async with AsyncClient(
        base_url="http://127.0.0.1:8001/api/v1",
        transport=transport,
    ) as test_client:
        yield test_client
