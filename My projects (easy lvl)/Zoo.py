from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, a_name, hungry):
        self.a_name = a_name
        self.__hungry = hungry

    def get_hungry(self):
        return self.__hungry
    
    def set_hungry(self, value):
        if self.get_hungry() == 100:
            print("Жывотное сыто")
            return
        
        if value >= 100:
            self.__hungry = 100
        else:
            self.__hungry = value


    @abstractmethod
    def make_sound(self):
        pass

class Lion(Animal):
    def __init__(self, a_name):
        super().__init__(a_name, hungry=50)

    def make_sound(self):
        print("Ррррр!")

class Parot(Animal):
    def __init__(self, a_name):
        super().__init__(a_name, hungry=50)

    def make_sound(self):
        print("Полли хочет креккер!")

class Wathcer:
    def __init__(self, w_name):
        self.w_name = w_name
        self.__food_stock = 5
    
    def get_food_stock(self):
        return self.__food_stock
    
    def feed_animal(self, animal):
        if self.get_food_stock() > 0:
            animal.set_hungry(animal.get_hungry() + 25)
            animal.make_sound()
            self.__food_stock -= 1
        else:
            print("Пополните запас еды!")

class Zoo:
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
        self.animals = []
    
    def add_animal(self, animal_info):
        self.animals.append(animal_info)

    def show_all_animal(self):
        for i in range(len(self.animals)):
            print(f"Name: {self.animals[i].a_name} | Hungry: {self.animals[i].get_hungry()}")

if __name__ == "__main__":
    yakuta_zoo = Zoo("Yakuta Zoo")
    stas = Wathcer("Стас")
    simba = Lion("Симба")
    kesha = Parot("Кеша")
    yakuta_zoo.add_animal(simba)
    yakuta_zoo.add_animal(kesha)
    yakuta_zoo.show_all_animal()
    for i in range(6):
        stas.feed_animal(simba)
        stas.feed_animal(kesha)
        yakuta_zoo.show_all_animal()