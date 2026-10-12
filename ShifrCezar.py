import cryptedCEZAR as cc
shyfr = input("Шифрувати (1), дешифрувати(2): ")
if shyfr == "1":
    text = input("Текст на шифрування: ")
    s = int(input("Ключ шифрування: "))
    result = cc.crypted(text, s)
elif shyfr == "2":
    text = input("Текст на дешифрування: ")
    s = int(input("Ключ дешифрування: "))
    result = cc.decrypted(text, s)
else:
    print("not")

print(f"Новий текст: {result}")