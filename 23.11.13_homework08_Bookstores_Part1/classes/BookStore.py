from pydantic import BaseModel, field_validator
from .BookItem import BookItem

class BookStore(BaseModel):
    bookstore_name: str
    book_shelf: list[BookItem]