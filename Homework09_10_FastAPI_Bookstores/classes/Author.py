from pydantic import BaseModel, field_validator
import re


class Author(BaseModel):
    name: str
    author_id: str

    @field_validator("name")
    @classmethod
    def check_valid_name(cls, name: str):
        assert name.istitle(), "Author's name needs to be normal capital case."
        return name

    @field_validator("author_id")
    @classmethod
    def check_valid_author_id(cls, author_id: str):
        pattern = r"[A-Z]{4}-[0-9]{4}"
        assert re.match(pattern, author_id) and len(author_id)==9, "Author ID is not valid following the format XXXX-YYYY, X is CAPITAL LETTER, Y is a number"
        return author_id
