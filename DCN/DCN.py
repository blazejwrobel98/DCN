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
                repository.StartUpdate()
            except:
                repository.Error("StartUpdate")
                input("Wciśnij dowolny przycisk aby kontynuować . . .")
                continue
        elif option == 2:
            try:
                repository.StopUpdate()
            except:
                repository.Error("StopUpdate")
                input("Wciśnij dowolny przycisk aby kontynuować . . .")
        elif option == 3:
             try:
                repository.Update()
             except:
                repository.Error("Update")
                input("Wciśnij dowolny przycisk aby kontynuować . . .")
        elif option == 4:
            try:
                repository.Statistics()
            except:
                repository.Error("Statistics")
                input("Wciśnij dowolny przycisk aby kontynuować . . .")
    except:
        print("Nie wybrano żadnej z dostępnych opcji, spróbuj jeszcze raz")
        input("Wciśnij dowolny przycisk aby kontynuować . . .")
        continue