import random

a = [None, 'Rock', 'Scissors', 'Paper']
b = int(input("Виберіть камінь[1] або ножиці[2] або бумагу[3] числом 1-3: "))
c = random.randint(1, 3)

if b == 1 and c == 3:
    print(f"{a[b]} vs {a[c]} Ви програли!")
elif b == 1 and c == 2:
    print(f"{a[b]} vs {a[c]} Ви вийграли!")
elif b == 1 and c == 1:
    print(f"{a[b]} vs {a[c]} Нічия!")
elif b == 2 and c == 1:
    print(f"{a[b]} vs {a[c]} Ви програли!")
elif b == 2 and c == 2:
    print(f"{a[b]} vs {a[c]} Нічия!")
elif b == 2 and c == 3:
    print(f"{a[b]} vs {a[c]} Ви вийграли!")
elif b == 3 and c == 1:
    print(f"{a[b]} vs {a[c]} Ви вийграли!")
elif b == 3 and c == 2:
    print(f"{a[b]} vs {a[c]} Ви програли!")
elif b == 3 and c == 3:
    print(f"{a[b]} vs {a[c]} Нічия!")
else:
    print("Не ломайте правила гри!")

