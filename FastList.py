sandwich = ['pastrami', 'florida', 'florenchia', 'pastrami', 'lexa', 'pastrami', 'krabsburger']

'''while 'pastrami' in sandwich:
    sandwich.remove('pastrami')'''
sandwich = [k for k in sandwich if k != 'pastrami' ]
chislo = [k for k in range(100) if k % 2 == 0]
print(sandwich)
print(chislo)