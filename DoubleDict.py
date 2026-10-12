users = {
    'Vova': {
        'first': 'petya',
        'last': 'petrasyan',
        'local': 'Krim'
    },
    'ntr': {
        'first': 'Nikita',
        'last': 'suvorov',
        'local': 'Sibir'
    },
    'Smile': {
        'first': 'Sasha',
        'last': 'polyvyaniy',
        'local': 'Kazakstan'
    }
}
for u_name, u_info in users.items():
    print(f"\nUserName: {u_name.title()}")
    full_name = f"{u_info['first']} {u_info['last']}"
    print(f"\tFullName: {full_name.title()}")
    print(f"\tLocation: {u_info['local'].title()}")
    