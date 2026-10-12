import os
from random import randint
import time

def prog_start(game_url:str):
    while True:
        time.sleep(1)
        random_int = randint(0, 100)
        print(f"Faking random namber is: {random_int}")
        if random_int == 67 :
            return os.startfile(game_url)

prog_start("steam://rungameid/632360")