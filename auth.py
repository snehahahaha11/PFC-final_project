from Utils import load_users, save_users, hash_password, strong_password, write_log, LOG_FILE

from datetime import datetime     #For handling date and time in log entries

import os #For file handling
import time #For handling time in account lockout

locked_accounts = {}  #Dictionary to keep track of locked accounts and their lockout expiration times

#Checking if the username is valid. 
def valid_username(username):  
    if len(username) < 3:       #username must be longer than 3 characters
        return False   #if the username is less than 3 characters long, ruling it as invalid username
    return True    #if the username is valid, ruling it as valid username

#This function registers a new user.
def register_user():
    users = load_users()  #lodas existing users from the file

    username = input("Enter username: ").strip()     #Ask the user for a valid username
    
    if username == "":   #Checking if the username is empty
        print("--Username cannot be empty.--")
        return  #if the username is empty, exit the function
    
    if len(username) < 3:  #has to be longer than 3 characters
        print("--Username must be at least 3 characters long.--")
        return  #if the username is not valid, exit the function

    if username in users:   #Checking if the username already exists
        print("--Username already exists. Please choose a new one.--")
        return
    
    password = input("Enter password: ").strip()  #user can now enter a password

    if password ==  "":  #Checking if the password is empty
        print("--Password cannot be empty.--")  #if the password is empty, let the user know that the password cannot be empty and exit the function
        return  #if the password is empty, exit the function

    if len(password)< 6:  #Checking if the password is at least 6 characters long
        print("--Password must be at least 6 characters long.--")
        return  #if the password is less than 6 characters long, exit the function  
    
    if not strong_password(password):       #Checking if the password is strong or not
        print("--Weak password. Must be at least 6 characters, a number, uppercase letter, and special character.--")
        return   #if the password is not strong, exit the function

    users[username] = {     #Creating a new user with the username 
        "password": hash_password(password)  #storeing th password as hash
    } 

    save_users(users)   #Saving the user to the JSON file
    print("--User registered successfully!--") #letting the user know that the registration was successful
    write_log("user " + username + " registered")  #writing a log entry for the registration event
    print("Time:", datetime.now())  #printing the time when the user registered

#allowing the user to login 
def login_user():    
    users = load_users()  #Loading existing users from the file

    attempts = 3   #Setting the number of login attempts to 3

    username = input("Enter username: ").strip() #Asking the user for their username

    if username == "":   #Checking if the username is empty
        print("--Username cannot be empty.--")
        return  False #if the username is empty, exit the function
    
    if username not in users:   #Checking if the username exists 
            print("--User not found.--")   
            return  False #if the username is not found, exit the function
        
    if username in locked_accounts:

        if time.time() < locked_accounts[username]:

            remaining = int(locked_accounts[username] - time.time())

            print(f"--Account temporarily locked. Try again in {remaining} seconds.--")

            return False

        else:
            del locked_accounts[username]

    while attempts > 0:   #While the user still has attempts left

        password = input("Enter password: ").strip()    #Checking if the password is empty

        if not password:    #Checking if the password is empty
            print("--Password cannot be empty.--")
            return  False  #if the password is empty, let the user know that the password cannot be empty and exit the function

        if users[username]["password"] == hash_password(password):       #checking if the password is righ
            print("--Login successful!--")
            print("Time:", datetime.now())  #printing the time when the user logged in
            write_log("user " + username + " logged in")  #writing a log entry for the login event
            return True #if the password is correct, let the user know that the login was successful

        else:
                attempts -= 1 #if the password is incorrect, decrease the number of attempts by 1
                
                print("--Incorrect password.--") 
                print("Attempts left:", attempts)   #if the password is incorrect, let the user know that the password is incorrect
                write_log("user " + username + " failed login attempt")  #writing a log entry for the failed login attempt 

    locked_accounts[username] = time.time() + 60

    print("--Too many failed attempts. Account locked for 60 seconds.--")
    write_log("account locked due to too many failed login attempts for user " + username)   #writing a log entry for the account lock event

    return False #if the user has no attempts left, return False to indicate that the login was unsuccessful

#allowing the user to update their password from old to new one.
def update_password():      
    users = load_users()  #loading existing users from the file

    username = input("Enter username: ").strip()    #Checking if the username is empty

    if username == "":   #Checking if the username is empty
        print("--Username cannot be empty.--")
        return  #if the username is empty, exit the function

    if username not in users:   #Checking if the username exists
        print("--User not found.--")
        return
    
    old_password = input("Enter current passowrd:  ").strip()    #Asking the user for their current password

    if old_password == "":    #Checking if the current password is empty
        print("--Current password cannot be empty.--")
        return  #if the current password is empty, letting the user know that it cannot be empty and exit

    if users[username]["password"] != hash_password(old_password):      #Checking if the current password is correct
        print("--Current password is incorrect.--")
        return    #if the current password is incorrect, letting the user knoe that it is incorrect and exit

    new_password = input("Enter new password: ").strip()    #Asking the user for a new password

    if new_password ==  "":  #Checking if the new password is empty
        print("--New password cannot be empty.--")
        return  #if the new password is empty, letting the user know that it cannot be empty and exit

    if hash_password(new_password) == users[username]["password"]:
        print("--New password cannot be the same as the current password.--")
        return  #if the new password is the same as the current password, letting the user know that it cannot be the same and exit 

    if len(new_password)< 6:  #Checking if the new password is at least 6 characters long
        print("--New password must be at least 6 characters long.--")
        return  #if the new password is less than 6 characters long, letting the user know that it is too short and exit

    if not strong_password(new_password):   #Checking if the new password is strong enough
        print("--Weak password. Must be at least 6 characters, a number and an uppercase letter.--")
        return  #if the new password is not strong enough, letting the user know that it is weak and exit

    confirm_password = input("Confirm new password: ").strip()   #Asking the user to confirm the new password   

    if confirm_password == "":    #Checking if the confirm password is empty
        print("--Confirm password cannot be empty.--")
        return  #if the confirm password is empty, letting the user know that it cannot be empty and exit

    elif new_password != confirm_password:   #Checking if the new password and confirm password match
        print("--Passwords do not match.--")
        return  #if the new password and confirm password do not match, letting the user know that they do not match and exit

    users[username]["password"] = hash_password(new_password)   #Updating the password for the user
    save_users(users)   #Saving the updated user information 

    print("--Password updated successfully!--") #letting the user know that the password was updated successfully
    print ("Time:", datetime.now())  #printing the time when the password was updated
    
#allowing the user to delete their account
def delete_user():
    users =  load_users()  #load existing users from the file

    username = input("Enter username: ").strip()    #Checking if the username is empty

    if username ==  "":  #Checking if the username is empty
        print("--Username cannot be empty.--")
        return   #if the username is empty, letting the user know that it cannot be empty and exit
    
    if username not in users:     #Checking if the username exists
        print("--User not found.--")
        return    #if the username is not found, letting the user know that it is not found and exit
    
    password = input("Enter password: ").strip()    #Asking the user for their password

    if users[username]["password"] != hash_password(password):      #Checking if the password is correct
        print("--Incorrect password.--")
        return  #if the password is incorrect, letting the user know that it is incorrect and exit
    
    confirm = input("Are you sure you want to delete this user? (yes/no): ").strip().lower()   #Asking the user to confirm the deletion

    if confirm != "yes":   #Checking if the user confirmed the deletion
        print("--User deletion cancelled.--")
        return  #if the user did not confirm the deletion, letting the user know that the deletion was cancelled and exit
    
    del users[username]   #Deleting the user from the dictionary

    save_users(users)   #Saving the updated user information

    write_log("user " + username + " deleted account")  #writing a log entry for the user deletion event

    print("--User deleted successfully!--") #letting the user know that the user was deleted successfully
    print("Time:", datetime.now())  #printing the time when the user was deleted    

#allowing the user to logout
def logout_user():    
    print("--Logout successful!--")
    print("Time:", datetime.now())  #printing the time when the user logged out

    write_log("user logged out")  #writing a log entry for the logout event
    input("Press Enter to continue...")  #Waiting for the user to press Enter before continuing

#allowing the user to view the log file
def view_log():  
    if not os.path.exists(LOG_FILE):    #Checking if the log file exists
        print("--No log file found yet.--")
        return  #if the log file does not exist, letting the user know that there is no log file and exit

    print("\n--- Audit Log ---")      #Printing the contents of the log file

    with open(LOG_FILE, "r") as file:           #Opening the log file in read mode and reading the contents
        content = file.read()      #Storing the contents of the log file in a variable

        if content == "":      #Checking if the log file is empty
            print("--Log file is empty.--")
       
        else:                         #If the log file is not empty, printing the contents of the log file
            print(content)

    input("Press Enter to return to menu...")    #Waiting for the user to press Enter before returning to the menu1
   
#allowing the user to clear the log file
def clear_log():  

    if not os.path.exists(LOG_FILE):  #checking if the log file exists
        print("--No log file found.--")
        return  #if the log file does not exist, letting the user know that there is no log file and exit

    confirm = input("Are you sure you want to clear the log? (yes/no): ").strip().lower()    #Asking the user to confirm the log clear action

    if confirm != "yes":   #Checking if the user confirmed the log clear action
        print("--Log clear cancelled.--")
        return   #if the user did not confirm the log clear action, letting the user know that the log clear was cancelled and exit

    open(LOG_FILE, "w").close()        #Clearing the log file by opening it in write mode and closing it immediately

    print("--Log cleared successfully.--")       #letting the user know that the log was cleared successfully
    write_log("log file cleared")       #writing a log entry for the log clear event
    print("Time:", datetime.now())  #printing the time when the log was cleared