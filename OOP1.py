class Wallet:
    def __init__(self, owner, currency):
        self.owner = owner
        self.currency = currency
        self.balance = 0  # Изначально денег нет

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"Вы пополнили баланс на: {amount} {self.currency}")
        

    def spend(self, amount):
        # Твой код здесь: проверь, хватает ли денег. 
        # Если да — уменьши баланс. Если нет — выведи предупреждение.
        if self.balance - amount < 0:
            print("Недостаточно средств!")
            return 
        else:
            self.balance = self.balance - amount
            print(f"С вашего баланса снято: {amount} {self.currency}")
            return
    

    def info(self):
        # Твой код здесь: напечатай информацию о кошельке
        print(f"Владелец: {self.owner} | Баланс: {self.balance} {self.currency}")


# --- Проверка работы (код ниже должен заработать без ошибок) ---

my_wallet = Wallet("Алексей", "EUR")

my_wallet.deposit(100)   # Положили 100 евро
my_wallet.spend(30)      # Потратили 30 евро
my_wallet.info()         # Должно вывести: Владелец: Алексей | Баланс: 70 EUR

my_wallet.spend(200)     # Попытка потратить больше, чем есть. 
                         # Должно вывести: Недостаточно средств!