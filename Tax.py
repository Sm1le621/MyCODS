from TaxiScamer import distance as d
while True:
    t = input("Введіть відстань у км: ")
    s = d(t)
    print(f"Оплата за послуги таксі: ${s}, Відстань: {t}km")