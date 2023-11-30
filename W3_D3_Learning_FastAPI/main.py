from fastapi import FastAPI #Import the FastAPI class from the fastapi library: https://fastapi.tiangolo.com/tutorial/first-steps/ , 
from typing import Union
from pydantic import BaseModel 

app = FastAPI() #Create an "app" object, and we create by calling the initialiser of the FastAPI class.

@app.get("/") #Calling the decorator function, meaning to add side effect to a particular function, @ is used to call some methods or functions.
async def root(): #we are adding the root function into the actual app object in line 4, so that when we make a root API request, we will execute the root function in line 9.
    return {"message": "Hello World"} #The decorator in line 6: When we make a GET request at root, then we execute the root function.


class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}") #We define Get API result from the app object of class FastAPI -> Adding to the app a new GET API.
def read_item(item_id: int, item:Item, item2: Item, item3: Union[Item, None] = None, q: Union[str, None] = None): #item3: using Union so  we have a power up whether we want to define the item3 or not.
    return {"item_id": item_id, "q": q, "item": item, "item2": item2}

#Upgrade the API - trying to giving an item with Body
@app.put("/items/{item_id}") #we cannot use Get again. Otherwise, it will overide the same path from line 11-13. Inside the string, item_id is put in {}, making FastAPI recognise item ID as a path parameters.
def update_item(item_id: int, item: Item): #it maps the ID path parameters to become the input variable for the update_item function.
    return {"item_id": item_id, "item": item}
















#>>> my_dictionary={"item_id": "1A2B", "q": None} (Python3)
#>>> print(my_dictionary)
#{'item_id': '1A2B', 'q': None}