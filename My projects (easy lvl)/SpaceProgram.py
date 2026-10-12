from abc import ABC, abstractmethod

class SpaceBoat(ABC):
    def __init__(self, name, speed, fuel):
        self.name = name
        self.speed = speed
        self.__fuel = fuel
        
    def get_fuel(self):
        return self.__fuel
        
    def set_fuel(self, value):
        if self.__fuel + value < 0:
            self.__fuel = 0
        elif self.__fuel + value > 100:
            self.__fuel = 100
        else:
            self.__fuel += value
            
    @abstractmethod
    def flight(self):
        pass
    
class CargoShip(SpaceBoat):
    def __init__(self, name, speed, fuel):
        super().__init__(name, speed, fuel)
        
    def flight(self):
        return "Летит медленно и достовляет груз."
            
class FighterShip(SpaceBoat):
    def __init__(self, name, speed, fuel):
        super().__init__(name, speed, fuel)
        
    def flight(self):
        return "Совершает прижок на гипер скорости."
        
class Captain:
    def __init__(self, name):
        self.name = name
        self.__fuel_box = 3
        
    def get_fuel_box(self):
        return self.__fuel_box
        
    def refill(self, refill_object):
        if self.__fuel_box > 0:
            refill_object.set_fuel(25)
            self.__fuel_box -= 1
            print(f"{self.name} заправил {refill_object.name} на 25%. Теперь канистр топлива: {self.__fuel_box}")
            return
        else:
            print("Нету канистр с топливом!")
            
class SpacePort:
    def __init__(self, name):
        self.name = name
        self.boats = []
        
    def save_boat(self, boat_obj):
        print(f"{boat_obj.name} прибыл в порт!")
        self.boats.append(boat_obj)
        
    def start_boats(self):
        for i in range(len(self.boats)):
            print(f"Name: {self.boats[i].name} | Fuel: {self.boats[i].get_fuel()}% | Status: {self.boats[i].flight()}")

if __name__ == '__main__':
    port = SpacePort("SpaceX")
    captain = Captain("Arnold•D•Carpus")
    fighter = FighterShip("Klaster", 750, 40)
    cargo = CargoShip("Tubo", 170, 40)
        
    port.save_boat(fighter)
    port.save_boat(cargo)
    captain.refill(cargo)
    port.start_boats()