print("~~Завдання а: ")
a = [9, 2, 5, 6]
a[0] = 12
b = sorted(a)
print(f"{a},\n{b}")

print("~~Завдання b: ")
c = [27, 3, 12, 22, 37, 8]
print(max(c))
c.pop(1)
d = sorted(c)
d.insert(3, 5)
d[0] = 10
print(f"{c}\n{d}")

print("~~Завдання c: ")
v = [5, 7, 8, 12, 4]
x = []
for i in v:
    if i > 5:
        x.append(i)

print(sum(x))

print("~~Завдання d: ")
g = [4, 6, 13, 9, 5, 16, 11]
j = []
for i in g:
    if i > 6:
        print(i * 2)
        j.append(i * 2)

print(f"Сумма чисел: {sum(j)}")