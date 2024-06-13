from typing import List

from pydantic import BaseModel

class UploadMemeResponse(BaseModel):
    """
    Pydantic schema for Upload meme data.

    Attributes:
    -----------
    - filename: meme's filename.
    - url: finalized url to s3 storage.
    """
    filename: str
    url: str

class MemeURLsResponse(BaseModel):
    """
    Pydantic schema for MemeURLs data.

    Attributes:
    -----------
    - urls: list of all s3 stored memes.
    """
    urls: List[str]
