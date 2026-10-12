cities = {
    'pervomaisk': {
        'country': 'Ukraine',
        'population': 64000,
        'fact': 'Первомайськ це 3 обєднаних села'
    },
    'mykolaiv': {
        'country': 'Ukraine',
        'population': 4806787,
        'fact': 'Північне причорноморя'
    },
    'Rio-de-ganeiro': {
        'country': 'Brazil',
        'population': 6300000,
        'fact': 'Статуя ісуса христа'
    }
}

for city, info in cities.items():
    print(f"\nCity{city.title()}:")
    for g, val in info.items():
        if g == 'coutry':
            print(f"{g}: {val.title()}")
        else:
            print(f"{g}: {val}")
