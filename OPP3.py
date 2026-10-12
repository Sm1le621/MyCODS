from abc import ABC, abstractmethod

class Order(ABC):
    def __init__(self, item_name, base_price):
        self.item_name = item_name
        self.base_price = base_price
        self.__delivery_fee = 150  # Инкапсулированное поле

    def get_delivery_fee(self):
        return self.__delivery_fee

    @abstractmethod
    def calculate_total(self):
        pass


class RegularOrder(Order):
    def calculate_total(self):
        return self.base_price + super().get_delivery_fee()


class VipOrder(Order):
    def __init__(self, item_name, base_price, discount):
        super().__init__(item_name, base_price)
        self.discount = discount

    def calculate_total(self):
        full_price = self.base_price + super().get_delivery_fee()
        return full_price * (1 - self.discount)


class Courier:
    def __init__(self, name):
        self.name = name
        self.delivered_orders = []

    def deliver(self, order_object):
        print(f"Курьер {self.name} доставил {order_object.item_name}. Итого к оплате: {order_object.calculate_total()} руб.")
        self.delivered_orders.append(order_object)


# --- Проверка работы ---
order1 = RegularOrder("Пицца", 500)
order2 = VipOrder("Суши Сет", 1200, 0.15)  # Скидка 15%

alex = Courier("Алексей")

print("--- Процесс доставки ---")
alex.deliver(order1)
# Ожидаемый вывод: Курьер Алексей доставил Пицца. Итого к оплате: 650 руб.

alex.deliver(order2)
# Ожидаемый вывод: Курьер Алексей доставил Суши Сет. Итого к оплате: 1147.5 руб. 
# (Так как (1200 + 150) * 0.85 = 1147.5)