class Car: 
    def __init__(self, brand, milage_km):
        self.brand = brand  
        self.milage_km = milage_km

    def  drive(self, distance_km): 
        self.milage_km = self.milage_km + distance_km 