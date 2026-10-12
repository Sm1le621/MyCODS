def crypted(text, s):
    alphabet = " АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    resul = ""
    for i in range(len(text)):
        char = text[i].upper()
        pos = alphabet.index(char)
        #print(pos)
        new_pos = (pos + s)%len(alphabet)
        resul += alphabet[new_pos]
    return resul

def decrypted(text, s):
    alphabet = " АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    resul = ""
    for i in range(len(text)):
        char = text[i].upper()
        pos = alphabet.index(char)
        #print(pos)
        new_pos = (pos - s)%len(alphabet)
        resul += alphabet[new_pos]
    return resul