from dataclasses import dataclass

@dataclass
class ItemOrigin: #nested dataclass: this class inside the class InventoryItem
    country: str
    production_date: str


@dataclass
class InventoryItem:
    name: str 
    quantity: int 
    serial_number: str
    origin: ItemOrigin 


def main():
    item_origin = ItemOrigin(country= "Ethiopia", production_date = "02/12/2023") #create object
    my_item1 = InventoryItem(name = "printer", 
                             quantity = 5, 
                             serial_number = "HDOUHKJN",
                             origin = item_origin)
    my_serialised_object1 = my_item1.__dict__
    print (my_serialised_object1)
    my_item2 = InventoryItem(**my_serialised_object1) #** break the object down into properties and passes them to InventoryItem
    print(my_item2.__dict__)



if __name__ == "__main__":
    main()

