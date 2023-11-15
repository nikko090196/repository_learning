from fastapi import FastAPI  # https://fastapi.tiangolo.com/tutorial/first-steps/
from typing import Union  # import other things like list, dictionary, set, final
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# template of engineer engine. The path is purely concerned with API of URL
@app.get("/items/{item_id}")
# Defaulting the value of "q" to None, kind of string. "q" does not need to be specified, can be none.
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# my_dict={"item_id":"1A!2B","q":None}
# print(my_dict)


#run uvicorn main:app --reload


class Item(BaseModel):
    name: str
    price: float

#upgrades
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return ("item_id":item_id, "item":item)