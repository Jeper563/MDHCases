from todolist import todolist
from random import randint
import sys
import os
import errno

lines = "-----------------------------------"

def errorproof():
    while True:
        try:
            enter = input("Press enter to continue.")
            if enter == "":
                break
            else:
                print("I said press enter to continue.")
        except (KeyboardInterrupt):
            print("I said press enter to continue.")


def clear(): os.system('cls')


def printlist():
    print(lines)
    for i in todolist:
        if i["checked"]:
            print(todolist.index(i), "| [X]", i["task"])
        else:
            print(todolist.index(i), "| [ ]", i["task"])
    print(lines)


def listtodo():
    printlist()
    errorproof()


def addtolist():
    print(lines)
    todoadd = input("Todo description >> ")
    todolist.append({"task": todoadd, "checked": False})
    print(lines+"\nSUCCESS: Added task", todoadd, "to the list.\n"+lines)
    errorproof()


def checktodo():
    printlist()
    while True:
        try:
            checkindex = int(input("Todo index >> "))
            todolist[checkindex]["checked"] = not todolist[checkindex]["checked"]
            print(lines)
            if todolist[checkindex]["checked"]:
                print("SUCCESS: Checked task", todolist[checkindex]["task"])
            else:
                print("SUCCESS: Unchecked task", todolist[checkindex]["task"])
            break
        except (ValueError, IndexError, KeyboardInterrupt):
            print("ERROR: Not a valid index")
    print(lines)
    errorproof()


def deletetodo():
    printlist()
    while True:
        try:
            deleteindex = int(input("Todo index >> "))
            tempstring = todolist[deleteindex]["task"]
            todolist.pop(deleteindex)
            break
        except (ValueError, IndexError, KeyboardInterrupt):
            print("ERROR: Not a valid index")
    print(lines+"\nSUCCESS: Deleted task", tempstring, "from list.\n"+lines)
    errorproof()


def savetodo():
    while True:
        try:
            option = int(input("Do you want to save your current todo list as a text file?\n0 | Yes\n1 | No\n>> "))
            messages = [
                "Saving...",
                "Cancelling...",
            ]
            print(messages[option])
            if option == 0:
                break
            else:
                errorproof()
                return
        except (ValueError, IndexError, KeyboardInterrupt):
            print("ERROR: Invalid input.")
    randomfilename = "./todolists/todolist"+str(randint(0, 999999))
    if not os.path.exists(os.path.dirname(randomfilename)):
        os.makedirs(os.path.dirname(randomfilename))
    saved = open(randomfilename, "x")
    for i in todolist:
        saved.write("\n")
        if i["checked"]:
            writtenstring = str("[X] | " + " " + i["task"])
        else:
            writtenstring = str("[ ] | " + " " + i["task"])
        saved.write(writtenstring)
    print("Saved to file", randomfilename[12:], "\n"+lines)
    saved.close()
    errorproof()


def loadtodo():
    directory = "./todolists"
    files = []
    visualfiles = []
    for entry in os.scandir(directory):
        visualentry = (str(entry)[11:-2])
        files.append(entry)
        visualfiles.append(visualentry)
    print("Choose one of the following files:")
    for i in range(len(visualfiles)):
        print(i, "|", visualfiles[i])
    while True:
        try:
            fileindex = int(input(">> "))
            chosenfile = files[fileindex]
            chosenvisualfile = visualfiles[fileindex]
            break
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Invalid input.")
    todolist.clear()
    loaded = open(chosenfile, "rt")
    for i in loaded:
        readstring = loaded.readline()
        if readstring[:2] == "[X":
            todolist.append({"task": readstring[6:], "checked": True})
        else:
            todolist.append({"task": readstring[6:], "checked": False})
    print("Loaded from file", chosenvisualfile, "\n"+lines)
    loaded.close()
    errorproof()


def exitprogram():
    f = open("todolist.py", "w")
    print("todolist =", todolist, file=f)
    sys.exit()


instructions = {
    "list": listtodo,
    "add": addtolist,
    "check": checktodo,
    "delete": deletetodo,
    "save": savetodo,
    "load": loadtodo,
    "exit": exitprogram,
}
clear()

infostring = ""

while True:
    print(
        "***********************************\n              Todoify\n"+lines+"\nlist   | List todos\nadd    | Add todo\ncheck  | Check todo"
        "\ndelete | Delete todo\n"+lines+"\nsave   | Save todos to file\nload   | Load todos from file\n"+lines+"\n"
        "exit   | Exit the program\n"+lines+"\n" + infostring)
    try:
        whattodo = input("Selection >> ")
        instructions[whattodo]()
        infostring = ""
    except (KeyError, KeyboardInterrupt):
        infostring = "ERROR: Invalid input.\n"
    clear()
