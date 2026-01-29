ground = [[], [], [],
          [], [], [],
          [], [], []]

wins = [
    (0,1,2), (3,4,5), (6,7,8),  
    (0,3,6), (1,4,7), (2,5,8),  
    (0,4,8), (2,4,6)           
]


def TicTacToe():
    while True:
        a = input("〰Виберіть символ (x, o)💨 ")
        if a != 'x' and a != 'o' and a != 'exit':
            print("💥💥Невірний символ💥💥")
            continue
        elif a == "exit": 
            print(f"\n {ground[0:3]}\n {ground[3:6]}\n {ground[6:9]}\n \n👋До зустрічі!👋")
            break
        
        b = int(input("〰Введіть число комірки (0-8)💨 "))

        if len(ground[b]) == 1:
            print(f"\n 😡Комірка зайнята!😡 \n")
            continue

        else:
            ground[b].append(a)
            print(f"\n {ground[0:3]}\n {ground[3:6]}\n {ground[6:9]}\n ")
        
        for w in wins:
            if ground[w[0]] == ground[w[1]] == ground[w[2]] == ['x']:
                print("✨🎉Ви виграли!🎉✨")
                return
            
            elif ground[w[0]] == ground[w[1]] == ground[w[2]] == ['o']:
                print("🔺🔻Ви програли!🔻🔺")
                return
            
        


TicTacToe()