import repository
import os

while True:
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
                repository.Wait()
                continue
        elif option == 2:
            try:
                repository.StopUpdate()
            except:
                repository.Error("StopUpdate")
                repository.Wait()
        elif option == 3:
             try:
                repository.Update()
             except:
                repository.Error("Update")
                repository.Wait()
        elif option == 4:
            try:
                repository.Statistics()
            except:
                repository.Error("Statistics")
                repository.Wait()
        elif option == "DEBUG":
            try:
                repository.DebugMenu()
            except:
                repository.Error("Debug")
                repository.Wait()
    except:
        print("Nie wybrano żadnej z dostępnych opcji, spróbuj jeszcze raz")
        repository.Wait()
        continue