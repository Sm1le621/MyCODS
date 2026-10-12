import random

password = []
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', '-', '_']
for i in range(0, 8):
    b = random.randint(0, len(a))
    password.append(a[b])

print("".join(password))
