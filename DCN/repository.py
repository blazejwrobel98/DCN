
def GlobalMenu():
    options = ["Start Update","Stop Update","Aktualizacja","Statystyki","Wyjście"]
    o = 0
    for i in range(len(options)):
        if options[i] =="Wyjście":
            print(f'[0] {options[i]}')
        else:
            o+=1
            print(f'[{o}] {options[i]}')
        
def Error(fun):
    print(f'Wystąpił błąd podczas wywoływania funkcji: {fun}')

def StartUpdate():
    stream = os.popen('screen -S update')
    output = stream.read()
    str(output)
    match = '(running)'