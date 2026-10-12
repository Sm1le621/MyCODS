text = input("Введіть текст: ")
stack = []

for i in text:
    if i == '(':
        stack.append(i)  
    elif i == ')':
        if not stack:
            print("Неправильно")  
        else:
            stack.pop()


if not stack:
    print("Правильно")
else:
    print("Неправильно")



