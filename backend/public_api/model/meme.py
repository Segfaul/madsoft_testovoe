from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from backend.public_api.validator import validate_link
from backend.public_api.model.base import Base
from backend.public_api.model.mixin import CRUDMixin


class Meme(Base, CRUDMixin):
    '''
    Meme instance

    Attributes
    ----------
    title : str
        meme's title
    description : str
        meme's description (optional)
    image_url : str
        meme's image_url
    created_at : datetime
        date the match was created
    '''
    __tablename__ = "meme"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    title: Mapped[str] = mapped_column(
        "title", String(length=64), nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(
        "description", String(length=128), nullable=True, default=None
    )
    image_url: Mapped[str] = mapped_column(
        "image_url", String(length=64), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    @validates('image_url')
    def validate_image_link(self, key, value):
        '''Validate link to http://host.domain/image.ext format'''
        if not validate_link(value):
            return ValueError("Provided incorrect image_url (http://host.domain/image.ext)")
        return value
