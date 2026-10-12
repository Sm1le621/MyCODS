from art import text2art
from colorama import Fore, Back, Style

text = input("Your text: ")
ascii_art = text2art(text)
print(Fore.BLUE)
print(ascii_art)

input("Enter для завершения програмы!")