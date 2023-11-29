from classes import IceCar, ElectricCar 

def main():
    my_ev = ElectricCar("Tesla",25000,500)
    my_ev.drive(distance_km = 3000)

    print(my_ev.__dict__)
    print(my_ev)
    print("")

    my_icecar = IceCar("Mercedes", 25000, 10, 80)

    print(my_icecar.__dict__)
    print(my_icecar)
    print("")

if __name__ =="__main__":
    main()
