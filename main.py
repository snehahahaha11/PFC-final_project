
#importing the functions from auth.py to main.py
from auth import register_user, login_user, update_password, logout_user, view_log, delete_user,clear_log
  

#This function shows menu and keeps running until the user chooses to exit
def main():

    logged_in = False #This variable keeps track of whether a user is logged in or not

    while True:   #This loop keeps the program running until the user chooses to exit
        print("\n============================================")
        print("        Secure Authentication System         ")
        print("============================================")
        print("1. Register")
        print("2. Login")
        print("3. Update Password")
        print("4. Logout")
        print("5. View Log")
        print("6. Delete Account")
        print("7. Clear Log")
        print("8. Exit")

        print("============================================")

#Asking the user to choose an option
        choice = input("Choose an option: ").strip() #Removing any leading or trailing whitespace from the user's input

#If the user chooses 1, run the registration function
        if choice == '1':
            register_user()

#If the user chooses 2, run the login function  
        elif choice == '2':  
            if login_user():    
                logged_in = True  #If login is successful, set logged_in to True

#If the user chooses 3, run the update password function
        elif choice == '3':
            update_password()

#If the user chooses 4, logout the user and exit the program
        elif choice == '4':
            
            if logged_in: 
                logout_user()
                logged_in = False  #Set logged_in to False after logging out
            else:   
                print("~No user is currently logged in.~")  #If no user is logged in, show an error message
                input("Press Enter to continue...")  #Wait for the user to press Enter before continuing
             
#If the user chooses 5, view the log file and exit the program
        elif choice =='5':
            view_log()  

#If the user chooses 6, run the delete user function
        elif choice == '6':  
             delete_user()    
                
#If the user chooses 7, clear the log file and exit the program
        elif choice == '7':
            clear_log()  
            
#If the user chooses 8, exit the program
        elif choice == '8':
            print("--Exit--")
            break 

        else:  #If the user enters an invalid option, show an error message
             print("~Invalid option. Please try again.~")

if __name__ == "__main__":  
    main()  #Running the main function to start the program 
 