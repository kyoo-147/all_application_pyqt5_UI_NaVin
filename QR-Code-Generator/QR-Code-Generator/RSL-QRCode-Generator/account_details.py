import re
import json
import hashlib


class Account:
    """A class used to create user accounts."""

    def __init__(self):
        """Initialise username and password attributes"""
        self.username = ""
        self.password = ""
        self.recoveryPassword = ""

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_recovery_password(self):
        return self.recoveryPassword

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_recovery_password(self, recoveryPassword):
        self.recoveryPassword = recoveryPassword

    def verify_account_creation(self):
        """Verify the username and password pass the required criteria"""
        username = self.get_username()
        password = self.get_password()
        f = 'Usernames.txt'
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        lines = []
        try:
            with open(f, "r") as file:
                # Read the binary file to a list to test the while loop
                lines = file.read().split('\n')

        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating file...")

        while True:
            if username in lines:
                print("Username is taken, please try again")
                username = input("Please enter a new username: ").upper()
                self.set_username(username)
                continue
            elif len(username) < 3 or len(username) > 12:
                print("Username length must be between 3 - 12 characters")
                username = input("Please enter a new username: ").upper()
                self.set_username(username)
                continue
            elif len(password) < 8:
                print("Password length must be greater than 8 characters long: ")
                password = input("Please enter a new password: ").upper()
                self.set_password(password)
                continue
            elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
                print("Password must contain a mixture of letters, numbers and special characters")
                password = input("Please enter a new password: ").upper()
                self.set_password(password)
                continue
            elif regex.search(password) is None:
                print("Password must contain special characters")
                password = input("Please enter a new password: ").upper()
                self.set_password(password)
                continue
            else:
                try:
                    with open(f, "a") as file:
                        file.write(username + '\n')
                # Throw exception if the file does not exist.
                except FileNotFoundError:
                    print("File does not exist, please contact support.")

                self.create_account()
                print("Account successfully created")
                break

    def create_account(self):
        """A function that will create the user account"""
        username = self.get_username()
        password = self.get_password()
        recoveryPassword = self.get_recovery_password()
        f = 'UserDetails.txt'
        ff = 'UserQuestion.txt'
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        hashed_recoveryPassword = hashlib.sha512(recoveryPassword.encode()).hexdigest()
        try:
            # Open the .bin file for writing - ('With open' automatically closes the file upon completion)
            with open(f, "a") as file:
                credentials = {'username': username, 'password': hashed_password}
                file.write(json.dumps(credentials) + "\n")
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, please contact support.")

        try:
            # Open the .bin file for writing - ('With open' automatically closes the file upon completion)
            with open(ff, "a") as file:
                credentials = {'username': username, 'recoveryPass': hashed_recoveryPassword}
                file.write(json.dumps(credentials) + "\n")
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, please contact support.")

    def verify_account_login(self, username, password):
        """Verifies the account details on login attempt"""
        search_key1 = "username"
        search_key2 = "password"
        username = username
        password = password
        f = "UserDetails.txt"
        counter = 0
        limit = 3
        # Read all the dictionaries from the file
        with open(f, "r") as file:
            dict_list = [json.loads(line) for line in file]

        # Modify the required dictionary

        while True:
            if counter >= limit:
                exit()
            match_found = False
            for dictionary in dict_list:
                if dictionary.get(search_key1) == username and hashlib.sha512(password.encode()).hexdigest() == dictionary.get(search_key2):
                    print("Login successful!")
                    match_found = True
                    break  # Stop searching after the first match is found
            if match_found:
                break  # Exit the loop if a match is found
            else:
                counter += 1
                print("Please re-enter your details.")
                search_key1 = "username"
                username = input("Please enter your username: ").upper()  # value1
                search_key2 = "password"
                password = input("Please enter your password: ").upper()  # value1
                continue

    def update_password(self):
        """Recover the users account and allows them to reset their details"""
        # Define the dictionary to be modified
        search_key1 = "username"
        search_value1 = input("Please enter your username: ").upper()  # value1
        search_key2 = "recoveryPass"
        search_value2 = input("Please enter your recovery password: ").upper()  # value1
        f = "UserQuestion.txt"
        ff = "UserDetails.txt"
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # Read all the dictionaries from the file
        with open(f, "r") as file:
            dict_list = [json.loads(line) for line in file]

        # Modify the required dictionary
        while True:
            match_found = False
            for dictionary in dict_list:
                if dictionary.get(search_key1) == search_value1 and hashlib.sha512(search_value2.encode()).hexdigest() == dictionary.get(search_key2):
                    print("A match is found!")
                    match_found = True
                    break  # Stop searching after the first match is found
            if match_found:
                break  # Exit the loop if a match is found
            else:
                print("A match could not be found, please re-enter your details.")
                search_key1 = "username"
                search_value1 = input("Please enter your username: ").upper()  # value1
                search_key2 = "recoveryPass"
                search_value2 = input("Please enter your recovery password: ").upper()  # value1
                continue

        modify_key = "password"
        new_value = input("Please enter a new password: ")

        while True:  # new_value is the new password
            if len(new_value) < 8:
                print("Password length must be greater than 8 characters long: ")
                new_value = input("Please enter a new password: ").upper()
                continue
            elif not (any(c.isalpha() for c in new_value) and any(c.isdigit() for c in new_value)):
                print("Password must contain a mixture of letters, numbers and special characters")
                new_value = input("Please enter a new password: ").upper()
                continue
            elif regex.search(new_value) is None:
                print("Password must contain special characters")
                new_value = input("Please enter a new password: ").upper()
                continue
            else:
                break  # Stop the while loop

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(new_value.encode()).hexdigest()

        # Read all the dictionaries from the file
        with open(ff, "r") as file:
            dict_list = [json.loads(line) for line in file]

        # Modify the required dictionary
        for dictionary in dict_list:
            if dictionary.get(search_key1) == hashed_password:
                dictionary[modify_key] = new_value
                break  # Stop searching after the first match is found

        # Write all the dictionaries back to the file
        with open(ff, "w") as file:
            for dictionary in dict_list:
                file.write(json.dumps(dictionary) + "\n")

        print("Password has been successfully changed.")

# TESTING

# while True:
#     my_account = Account()
#
#     # Welcome statement.
#     print("~ Welcome, please sign-in or create an account ~")
#     option = input("Enter A to Sign-in | Enter B to Create Account | Enter C to Recover Account: ")
#     # While the input is not equal to displayed options - loop.
#     while option.upper() != "A" and option.upper() != "B" and option.upper() != "C":
#         print("Incorrect input, please try again.")
#         option = input("Enter A to Sign In | Enter B to Create Account | Enter C to Recover Account: ")
#     # If input equals A, run the sign-in process
#     if option.upper() == "A":
#         print("Please enter your account details: ")
#         username = input("Username: ").upper()
#         password = input("Password: ").upper()
#         my_account.verify_account_login(username, password)
#         break
#     # If input equals CUSTOMER, run the customer function.
#     elif option.upper() == "B":
#         username = input("Username: ").upper()
#         password = input("Password: ").upper()
#         accountRecoveryPassword = input("Account Recovery Password: ").upper()
#         my_account.set_username(username)
#         my_account.set_password(password)
#         my_account.set_recovery_password(accountRecoveryPassword)
#         my_account.verify_account_creation()
#         continue
#     elif option.upper() == "C":
#         my_account.update_password()
#         continue