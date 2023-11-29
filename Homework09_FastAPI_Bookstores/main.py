from classes import Author, BookItem, BookStore
from pydantic import ValidationError 
from fastapi import FastAPI, HTTPException 
from typing import Dict

app = FastAPI()


my_book_items_dict: Dict[str, BookItem] = {}

@app.put("/books/{name}")
def create_book(name:str, book1: BookItem):
    my_book_items_dict[name] = book1 
    print(my_book_items_dict)

@app.get("/books/{name}")
def get_book(name:str): 
    if name in my_book_items_dict.keys():
        return my_book_items_dict[name] 
    else:
        raise HTTPException(status_code = 404, detail="Book Item not found: "+name)

    