import repository
import os

while True:
    try:
        os.system('cls')    # For Windows
    except:
        continue
    try:
        os.system('clear')  # For Linux/OS X
    except:
        continue
    repository.GlobalMenu()
    try:
        option = int(input())
        if option == 0:
            print("Zamykanie Menu")
            break
        elif option == 1:
            try:
                repository.Install()
            except:
                repository.Error("Install")
                os.system("PAUSE")
                continue
        elif option == 2:
            try:
                repository.StartUpdate()
            except:
                repository.Error("StartUpdate")
                os.system("PAUSE")
                continue
        elif option == 3:
            try:
                repository.StopUpdate()
            except:
                repository.Error("StopUpdate")
                os.system("PAUSE")
        elif option == 4:
            try:
                repository.Update()
            except:
                repository.Error("Update")
                os.system("PAUSE")
        elif option == 5:
            try:
                repository.Statistics()
            except:
                repository.Error("Statistics")
                os.system("PAUSE")
    except:
        print("Nie wybrano żadnej z dostępnych opcji, spróbuj jeszcze raz")
        os.system("PAUSE")
        continue