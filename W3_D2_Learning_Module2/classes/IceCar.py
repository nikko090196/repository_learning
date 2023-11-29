from .Car import Car

class IceCar(Car):
    def __init__(self, brand, milage_km, fuel_consumption, fuel_level):
        Car.__init__(self, brand, milage_km) #initialise class Car bringin in the Clar clas variables, then we bring in IceCar class attributes with self.
        self.fuel_consumption = fuel_consumption
        self.fuel_level = fuel_level 