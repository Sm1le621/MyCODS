unconfirmed_users = ['14578' 'Disher', 'ntr', 'SM1le', 'Hoger', 'rONgs', 'gun', 'skif']
confirmed_users = []

while unconfirmed_users:
    user = unconfirmed_users.pop()
    if '5' not in user:
        print(f"Пройшов: {user}")
        confirmed_users.append(user)

pets = ['cat', 'dog', 'rabit', 'fish', 'cat' 'tiger', 'lion', 'cat']
print(pets)

while 'cat' in pets:
    pets.remove('cat')
print(pets)