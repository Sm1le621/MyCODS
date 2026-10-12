from random import randint

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
        n = randint(0, 8)
        if len(ground[n]) == 1:
            n = randint(0, 8)
            continue
        else:
            ground[n].append('o')
            print(f"\n {ground[0:3]}\n {ground[3:6]}\n {ground[6:9]}\n🤖Your turn!🤖")
        
        count = 0
        for j in ground:
            if len(j) == 1:
                count += 1
                if count == 9:
                    print("🏳️🤖!DRAW!🧑‍🦱🏳️")
                    return

        b = input("〰Please enter cell number(0-8 or exit)💨 ")

        if b == "exit": 
            print(f"\n {ground[0:3]}\n {ground[3:6]}\n {ground[6:9]}\n \n👋Goodbye!👋")
            return

        elif len(ground[int(b)]) == 1:
            print(f"\n 😡The cell is busy!😡 \n")
            continue

        else:
            ground[int(b)].append('x')
            print(f"\n {ground[0:3]}\n {ground[3:6]}\n {ground[6:9]}\n ")

        for w in wins:
            if ground[w[0]] == ground[w[1]] == ground[w[2]] == ['x']:
                print("✨🎉!WIN!🎉✨")
                return
            
            elif ground[w[0]] == ground[w[1]] == ground[w[2]] == ['o']:
                print("🔺🔻!LOSE!🔻🔺")
                return
            
        


TicTacToe()
