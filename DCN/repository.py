import os

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
    try:
        os.popen('screen -dm bash -c "python3.8 run.py')
        line = os.popen('screen -ls | grep update')
        output=line.read()
        str(output)
        match = "update"
        if (match in output):
            print('Pomyślnie uruchomiono usługę Update')
    except:
        print('Wystąpił błąd podczas uruchamiania usługi Update')