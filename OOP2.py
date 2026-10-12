class Subscription:
    def __init__(self, owner_name, monthly_cost):
        self.owner_name = owner_name
        self.monthly_cost = monthly_cost
        self.is_active = True

    def get_features(self):
        return "Доступ к фильмам в качестве 720p"

    def calculate_annual_cost(self):
        return self.monthly_cost * 12


class PremiumSubscription(Subscription):
    def __init__(self, owner_name, monthly_cost, cashback_rate):
        super().__init__(owner_name, monthly_cost)
        self.cashback_rate = cashback_rate

    def get_features(self):
        return "Доступ к фильмам в 4K Ultra HD + Просмотр без рекламы"

    def calculate_annual_cost(self):
        discount = super().calculate_annual_cost() * 0.15
        return super().calculate_annual_cost() - discount


def show_subscription_info(sub_object):
    print(f"Пользователь: {sub_object.owner_name} | Возможности: {sub_object.get_features()} | Стоимость за год: {sub_object.calculate_annual_cost()}")

# --- Проверка работы ---
basic = Subscription("Алексей", 10)
premium = PremiumSubscription("Мария", 20, 0.1)

print("--- Информация о подписках ---")
show_subscription_info(basic)
# Ожидаемый вывод:
# Пользователь: Алексей | Возможности: Доступ к фильмам в качестве 720p | Стоимость за год: 120

show_subscription_info(premium)
# Ожидаемый вывод (учитывая скидку 15% от 240):
# Пользователь: Мария | Возможности: Доступ к фильмам в 4K Ultra HD + Просмотр без рекламы | Стоимость за год: 204.0