import os

#input_mode = input()

#if input_mode == "1":
    
    #os.system("python input.py")
    
#if input_mode == "2":
    
    #os.system("python list_creators.py")
    
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main_menu():
    while True:
        clear()
        print("=== MAIN MENU ===")
        print("1. View image")
        print("2. List creator's posts")
        print("q. Quit Program")

        choice = input("-> ")

        if choice == "1":
               os.system("python post_image.py") # go to the image program
        if choice == "2":
               os.system("python list_creators.py") # go to the list program
        elif choice == "q":
            break               # exit program

main_menu()