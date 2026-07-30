from abc import ABC, abstractmethod 

class Character(ABC):
    def __init__(self, char_name, attack_power, health):
        self.char_name = char_name
        self.attack_power = attack_power
        self.__health = health
    
    def get_health(self):
        return self.__health
    
    def set_health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    def is_alive(self):
        if self.get_health() == 0:
            return False
        
        return True

    @abstractmethod
    def attack(self, target):
        pass

class Warrior(Character):
    def __init__(self, char_name):
        super().__init__(char_name, attack_power=20, health=100)

    def attack(self, target):
        target.set_health(target.get_health() - self.attack_power)
        print(f"{self.char_name} рубит мечом {target.char_name} и наносит {self.attack_power} урона!")

class Mage(Character):
    def __init__(self, char_name):
        super().__init__(char_name, attack_power=10, health=70)
        self.mana = 30

    def attack(self, target):
        if self.mana >= 10:
            self.mana - 10
            target.set_health(target.get_health() - (self.attack_power * 3))
            print(f"{self.char_name} пускает огненый шар в {target.char_name} и наносит {self.attack_power * 3} урона!")
        else:
            target.set_health(target.get_health() - self.attack_power)
            self.mana += 10
            print(f"{self.char_name} бьет посохом {target.char_name} на {self.attack_power} урона и восстанавливает 10 маны!")

class Monster(Character):
    def __init__(self, char_name):
        super().__init__(char_name, attack_power=15, health=120)

    def attack(self, target):
        target.set_health(target.get_health() - self.attack_power)
        print(f"{self.char_name} кусает {target.char_name} и наносит {self.attack_power} урона!")


# --- ЗАПУСК ИГРЫ ---
if __name__ == "__main__":
    print("--- ДОБРО ПОЖАЛОВАТЬ В ООП-RPG --- \n")
    
    # 1. Создаем персонажей
    player = Mage("Гэндальф")  # Можешь заменить на Warrior("Конан")
    boss = Monster("Дракон Смауг")
    
    print(f"БИТВА НАЧАЛАСЬ! {player.char_name} ({player.get_health()} HP) против {boss.char_name} ({boss.get_health()} HP) \n")
    
    # 2. Цикл битвы, пока оба живы
    round_num = 1
    while player.is_alive() and boss.is_alive():
        print(f"--- Раунд {round_num} ---")
        
        # Игрок бьет монстра
        player.attack(boss)
        
        # Если монстр выжил после удара игрока — он бьет в ответ
        if boss.is_alive():
            boss.attack(player)
            
        print(f"Статус после раунда: {player.char_name}: {player.get_health()} HP | {boss.char_name}: {boss.get_health()} HP\n")
        round_num += 1
        
    # 3. Финал битвы
    print("=========================")
    if player.is_alive():
        print(f"ПОБЕДА! {player.char_name} одолел монстра!")
    else:
        print(f"ИГРА ОКОНЧЕНА. {boss.char_name} оказался сильнее...")



        