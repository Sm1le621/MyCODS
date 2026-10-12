def person(username, country, age=None):
    person = {
        'username': username,
        'country': country
        }
    if age:
        person['age'] = age
    return person

mus = person('nikita', 'poland', age=14)
mus = person('Sanya', 'Ukraine', age=13)
print(mus)