from typing import List

from fastapi import APIRouter, Depends, Path, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.public_api.service.db_service import get_session
from backend.public_api.util import get_object_or_raise_404, create_object_or_raise_400, \
    update_object_or_raise_400, process_query_params, cache
from backend.public_api.model import Meme
from backend.public_api.schema import MemeSchema, PartialMemeSchema, MemeResponse

router = APIRouter(
    prefix="/v1/meme",
    tags=['Meme']
)

@router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[MemeResponse], response_model_exclude_unset=True
)
@cache(expire=300)
async def read_all_memes(
    request: Request,
    db_session: AsyncSession = Depends(get_session)
):
    query_params: dict = process_query_params(request)
    return [
        MemeResponse(**meme.__dict__).model_dump(exclude_unset=True) \
        async for meme in Meme.read_all(
            db_session,
            **query_params
        )
    ]


@router.get(
    "/{meme_id}", status_code=status.HTTP_200_OK,
    response_model=MemeResponse, response_model_exclude_unset=True
)
@cache(expire=60)
async def read_meme(
    request: Request,
    meme_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    meme = await get_object_or_raise_404(
        db_session, Meme, meme_id
    )
    return MemeResponse(**meme.__dict__).model_dump(exclude_unset=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=MemeResponse, response_model_exclude_unset=True
)
async def create_meme(
    request: Request,
    payload: MemeSchema,
    db_session: AsyncSession = Depends(get_session)
):
    meme = await create_object_or_raise_400(db_session, Meme, **payload.model_dump())
    return MemeResponse(**meme.__dict__).model_dump(exclude_unset=True)


@router.patch(
    "/{meme_id}", status_code=status.HTTP_200_OK,
    response_model=MemeResponse, response_model_exclude_unset=True
)
async def update_hero(
    request: Request,
    payload: PartialMemeSchema, meme_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    meme = await get_object_or_raise_404(db_session, Meme, meme_id)
    await update_object_or_raise_400(db_session, Meme, meme, **payload.model_dump())
    return MemeResponse(**meme.__dict__).model_dump(exclude_unset=True)


@router.delete(
    "/{meme_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_hero(
    request: Request,
    meme_id: int = Path(...),
    db_session: AsyncSession = Depends(get_session)
):
    meme = await get_object_or_raise_404(db_session, Meme, meme_id)
    await Meme.delete(db_session, meme)
