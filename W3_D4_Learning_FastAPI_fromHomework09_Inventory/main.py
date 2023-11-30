from dto import InventoryItem, ItemOrigin
from fastapi import FastAPI, HTTPException
from typing import Dict, List

app = FastAPI()

# Create a dictionary to store item:
# The key is string, and the value is InventoryItem, ={} starts the dictionary with an empty key-value pair.
my_inventory_item_dict: Dict[str, InventoryItem] = {}


@app.put("/inventoryitems/{serial_number}")
def create_item(serial_number: str, item1: InventoryItem) -> None: #Type hint with None as we do not return anything.
    my_inventory_item_dict[serial_number] = item1
    print(my_inventory_item_dict)


@app.get("/inventoryitems/{serial_number}")
# We do not need the body here, only need serial number for path params
def get_item(serial_number: str) -> InventoryItem: #Return this InventoryItem type
    if serial_number in my_inventory_item_dict.keys():
        # access the value of the item that has the valid key.
        return my_inventory_item_dict[serial_number]
    else:
        raise HTTPException(
            status_code=404, detail="Item not found: "+serial_number)


@app.delete("/inventoryitems/{serial_number}")
def delete_item(serial_number: str) -> Dict: #Return the message -> the Dict type
    # use the same FLOW CONTROL as GET request.
    if serial_number in my_inventory_item_dict.keys():
        my_inventory_item_dict.pop(serial_number)
        print(my_inventory_item_dict)
        return {"Message: Successfuly Deleted"}
    else:
        raise HTTPException(
            status_code=404, detail="Item not found: "+serial_number)


# Create a get API to return multiple items:
@app.get("/inventoryitems/") #We don't have a serial number as we want to try to get all items.
def get_items() -> List[InventoryItem]: #Hint the output of this function
    return my_inventory_item_dict.values() 
# You call .value() -> You can convert all the values of the dict into a list of all the dict, instead of returning the object/dict.
# We want just a list of values.
