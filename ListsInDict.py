fav_lang = {
    'nikita': ['c+', 'python', 'css', 'alien'],
    'lexa': ['python', 'java', 'c++'],
    'sasha': ['python' 'java']
}
fav_lang['egor'] = ['c']
for i, y in fav_lang.items():
    if len(y) > 1:
        print(f"{i.title()} favorite languages are:")
    else:
        print(f"{i.title()} favorite languages is:")
    for k in y:
        print(f"{k.title()}")
