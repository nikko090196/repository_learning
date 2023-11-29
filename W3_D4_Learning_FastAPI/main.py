from dto import InventoryItem, ItemOrigin 
from fastapi import FastAPI, HTTPException 
from typing import Dict

app = FastAPI()

#Create a dictionary to store item:
my_inventory_item_dict: Dict[str, InventoryItem] = {} #The key is string, and the value is InventoryItem, ={} starts the dictionary with an empty key-value pair.


@app.put("/items/{serial_number}")
def create_item(serial_number:str, item1: InventoryItem):
    my_inventory_item_dict[serial_number] = item1 
    print(my_inventory_item_dict)

@app.get("/items/{serial_number}")
def get_item(serial_number:str): #We do not need the body here, only need serial number for path params
    if serial_number in my_inventory_item_dict.keys():
        return my_inventory_item_dict[serial_number] #access the value of the item that has the valid key.
    else:
        raise HTTPException(status_code = 404, detail="Item not found: "+serial_number)



