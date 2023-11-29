from .Car import Car

class ElectricCar(Car): #subclass of Car with inherited properties and methods of Car class
     def __init__(self, brand, milage_km, range):
         super().__init__(brand, milage_km) #initalise the attribute of the parent's class
         self.range = range 