import json #For handling JSON data
import hashlib    #For hashing passwords
import os      #For file handling
from datetime import datetime     #For handling date and time in log entries

DATABASE_FILE = "users.json"  #File where user data is stored
LOG_FILE = "audit.log"  #File where log entries are stored

#This function loads users from the JSON file. 
def load_users():            
    if os.path.exists(DATABASE_FILE):   #checking if the file still exists

        with open(DATABASE_FILE, "r") as file:  #Openinig the file and reading the data
            return json.load(file)    #returning the data as a dictionary
    return {}

#This function saves the users to the JSON file.
def save_users(users):      #this  function takes data from iuser dictionary and saves it to the json file

    with open(DATABASE_FILE, "w") as file:   #Openinig the file in write-mode
        json.dump(users, file, indent=4)    #Save the user dictionary 

#This function converts the password into a hash 
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()  #Hashing the password 

#Checking if the password us strong enough.
def strong_password(password):  

    has_number = any(char.isdigit() for char in password)  #Checking if the password has at least one number
    has_upper = any(char.isupper() for char in password)    #Checking if the password has at least one uppercase letter
    has_special = any(not char.isalnum() for char in password)  #Checking if the password has at least one special character

    return has_number and has_upper and has_special   #If password has all three requirements, ruling it as strong password

#this functions writes messages to the log file with a timestamp.
def write_log(message):

    with open(LOG_FILE, "a") as log_file:  #Openinig the log file in append mode
        log_file.write(f"{datetime.now()}: {message}\n")  #Writing the log message with timestamp