from classes import Author, BookItem, BookStore
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException
from typing import Dict, List

app = FastAPI()

my_book_items_dict: Dict[str, BookItem] = {}

# Put API Request:


@app.put("/books/{name}")
def create_book(name: str, book1: BookItem) -> None:
    my_book_items_dict[name] = book1
    print(my_book_items_dict)
    return my_book_items_dict[name]


# Get API Request:


@app.get("/books/{name}")
def get_book(name: str) -> BookItem:
    if name in my_book_items_dict.keys():
        return my_book_items_dict[name]
    else:
        raise HTTPException(status_code=404, detail="Book Item not found: " + name)


# Delete API Request:


@app.delete("/books/{name}")
def delete_item(name: str) -> Dict:
    if name in my_book_items_dict.keys():
        my_book_items_dict.pop(name)
        print(my_book_items_dict)
        return my_book_items_dict
    else:
        raise HTTPException(status_code=404, detail="Book Item not found: " + name)


# Get API Request to return all books:


@app.get("/books/")
def get_items() -> List[BookItem]:
    return my_book_items_dict.values()
