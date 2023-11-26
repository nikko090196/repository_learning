from dto import InventoryItem, ItemOrigin 

from typing import Dict, List
from fastapi import FastAPI, HTTPException 

app = FastAPI()

my_inventory_items_dict: Dict[str, InventoryItem] = {} # {}equal to empty dictionary

@app.put("/items/{serial_num}")
def create_item(item: InventoryItem, serial_num: str) -> None: 
    my_inventory_items_dict[serial_num] = item 
    print(my_inventory_items_dict)

@app.get("/items/{serial_num}")
def get_item(serial_num: str) -> InventoryItem:
    if serial_num in my_inventory_items_dict.keys():
        return my_inventory_items_dict[serial_num]
    else:
        raise HTTPException(status_code=404, detail="Item not found: " + serial_num)

@app.delete("/items/{serial_num}")
def delete_item(serial_num: str) -> Dict:
    if serial_num in my_inventory_items_dict.keys():
        my_inventory_items_dict.pop(serial_num)
        print(my_inventory_items_dict)
        return "Successfully Deleted"
    else:
        raise HTTPException(status_code=404, detail="Item not found: " + serial_num)
    
app.get("/items/")
def get_items() -> List[InventoryItem]:
    return my_inventory_items_dict.values() 
