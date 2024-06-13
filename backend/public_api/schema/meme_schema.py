from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.public_api.util import _AllOptionalMeta


class MemeSchema(BaseModel):
    """
    Pydantic schema for Meme table data.

    Attributes:
    -----------
    - title: meme's title.
    - description: memes' description (optional).
    - image_url: meme's image_url.
    """
    title: str
    description: Optional[str] = None
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class PartialMemeSchema(MemeSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Meme table data (PATCH). 
    """


class IndependentMemeSchema(MemeSchema):
    """
    Pydantic schema for Meme table data (subqueries).

    Attributes:
    -----------
    - id: unique identifier of the meme.
    - title: meme's title.
    - description: meme's description (optional).
    - image_url: meme's image_url.
    - created_at: date the meme was created.
    """
    id: int
    created_at: datetime


class MemeResponse(IndependentMemeSchema):
    """
    Pydantic schema for Meme table data.

    Attributes:
    -----------
    - id: unique identifier of the meme.
    - title: meme's title.
    - description: meme's description (optional).
    - created_at: date the meme was created.
    """
