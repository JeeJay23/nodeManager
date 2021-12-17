print("Booting...")

import os
import meshctlwrapper

# test.connectNetwork()

### FUNCTIONS ###

def display_title_bar():
    # clears the terminal screen, and displays a title bar.
    os.system('clear')
              
    print("\t**********************************************")
    print("\t***          Node application              ***")
    print("\t**********************************************")
    
def get_user_choice():
    # let user know what they can do.
    print("\n[1] Show nodes")
    print("[2] Set led ")
    print("[3] get led state ")
    print("[q] Quit.")
    
    return input("Choose option. \n")

def showNodes():
    meshctlwrapper.getAllNodes()
    return 0

def setLight():
    meshctlwrapper.toggleLight(input("which element? "), input("on(1) or off(0)? "))

### MAIN PROGRAM ###
choice = ''
display_title_bar()
while choice != 'q':    
    
    choice = get_user_choice()
    # respond to the user's choice.

    if choice == '1':
        showNodes()
    elif choice == '2':
        setLight()
    elif choice == '3':
        # het is laat maar het is af
        print("state is: " + str(meshctlwrapper.getget(input("which node to query? "))))
    elif choice == 'q':
        print("\nExiting application")
        exit()
    else:
        print("\nWrong option\n")