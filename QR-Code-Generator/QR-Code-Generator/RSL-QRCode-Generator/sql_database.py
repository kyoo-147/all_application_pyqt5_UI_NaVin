import sqlite3
from servicemen import Serviceman


class SqlDatabase:
    """A database class required for sqlite functionality"""

    def __init__(self):
        """Initialise attributes for supermarket class"""
        self.db = ""

    def setup_db(self):
        """Create the database"""
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()

            # Creating the new servicemen table within the checkout_db.
            cursor.execute('''CREATE TABLE IF NOT EXISTS 
                  servicemen(serviceNumber CHAR(20) PRIMARY KEY, firstName CHAR(25), givenNames CHAR(50), lastName Char(25))''')

            cursor.execute(
                "INSERT INTO servicemen(serviceNumber, firstName, givenNames, lastName) VALUES ('R28159', 'KENNETH', 'ROY', 'BRYANT')")
            self.db.commit()

        # Except block to catch any errors that may occur.
        except Exception as e:
            print(f"Unable to create the table requested. {e}")
            self.db.rollback()
        # Close the database.
        finally:
            self.db.close()

    def insert_data(self, Serviceman):
        """The function adds servicemen details to the servicemen table in the checkout_db.db"""
        # Open the database with a try block and using an insert query, insert the serviceman object data into the servicemen table.
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()
            cursor.execute('''INSERT INTO servicemen(serviceNumber, firstName, givenNames, lastName) VALUES(?,?,?,?)''',
                           (Serviceman.get_service_number(), Serviceman.get_first_name(), Serviceman.get_given_names(),
                            Serviceman.get_last_name()))
            self.db.commit()
            print("The Data was successfully inserted.")
        # Except block to display any errors that may occur.
        except Exception as e:
            print(f"An error has occurred. {e}")
        # Close the database.
        finally:
            self.db.close()

    def drop_data(self, serviceNumberInput):
        """The function drops servicemen details from the database using the servicemen number as an input"""
        # Convert the input into a tuple in order to match the data type of the imported list.
        deleteUser = (serviceNumberInput,)
        importList = []
        serviceNumberToDelete = ""
        match_found = False
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()
            cursor.execute('''SELECT serviceNumber FROM servicemen''')
            rows = cursor.fetchall()
            if rows is None:
                return None
            else:
                # Append each row of the serviceNumber field from the servicemen database into a list.
                for row in rows:
                    importList.append(row)
                # Search that list for a match.
                for item in importList:
                    # If a match occurs, convert the search from a tuple into a string ready to be used in the SQL query.
                    if item == deleteUser:
                        for item in deleteUser:
                            serviceNumberToDelete = serviceNumberToDelete + item
                        # Once converted run the query.
                        cursor.execute('''DELETE FROM servicemen WHERE serviceNumber = ? ''',
                                       (serviceNumberToDelete,))
                        self.db.commit()
                        match_found = True
                # Output a statement based on whether a match is found or not.
                if match_found:
                    print(f"{serviceNumberToDelete} was successfully deleted from the servicemen database.")
                else:
                    print("The Service number entered was not found please try again.")
        except Exception as e:
            print(f"An error has occurred. {e}")
        # Close the database.
        finally:
            self.db.close()

    def search_database_serviceNumber(self, serviceNumber):
        """The function is required for searching the database using just the serviceNumber as an input"""
        # Convert the serviceNumber string into a list.
        serviceNumber = [serviceNumber]
        # Open the database with a try block and using a select query return the serviceNumber, firstName, givenNames, and lastName using the [serviceNumber] data.
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()
            cursor.execute(
                '''SELECT serviceNumber, firstName, givenNames, lastName FROM servicemen WHERE serviceNumber = ?''',
                serviceNumber)
            rows = cursor.fetchone()
            # If no rows can be found return nothing, else return a products.
            if rows == None:
                return None
            else:
                rows2 = list(rows)
                servicemen = Serviceman(rows2[0], rows2[1], rows2[2], rows2[3])
                return servicemen
        # Except block to display any errors that may occur.
        except Exception as e:
            print(f"An error has occurred. {e}")
        # Close the database.
        finally:
            self.db.close()

    def search_database_first_last_name(self, firstName, lastName):
        """The function is required for searching the database using just the serviceNumber as an input"""
        servicemen_list = []
        # Convert the serviceNumber string into a list.
        # Open the database with a try block and using a select query return the serviceNumber, firstName, givenNames, and lastName using the [serviceNumber] data.
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()
            cursor.execute(
                '''SELECT serviceNumber, firstName, givenNames, lastName FROM servicemen WHERE firstName = ? AND lastName = ?''',
                (firstName, lastName))
            rows = cursor.fetchall()
            # If no rows can be found return nothing, else return a products.
            if rows == None:
                return None
            else:
                for row in rows:
                    servicemen_list.append(Serviceman(row[0], row[1], row[2], row[3]))
        # Except block to display any errors that may occur.
        except Exception as e:
            print(f"An error has occurred. {e}")
        # Close the database.
        finally:
            self.db.close()
            return servicemen_list

    def list_all_servicemen(self):
        """Lists all transactions in the transactions table in the checkout_db.db"""
        # Open the database with a try block and using a select query, select all transaction data ordered by date.
        servicemen_list = []
        try:
            self.db = sqlite3.connect('servicemen_db.db')
            cursor = self.db.cursor()
            cursor.execute('''SELECT * FROM servicemen''')
            rows = cursor.fetchall()
            # If no rows can be found return nothing, else return a list of transactions.
            if rows is None:
                return None
            else:
                for row in rows:
                    servicemen_list.append(Serviceman(row[0], row[1], row[2], row[3]))
        # Except block to display any errors that may occur.
        except Exception as e:
            print(f"An error has occurred. {e}")
        # Close the database.
        finally:
            self.db.close()
            # Call the selection sort algorithm to sort the list in ascending order based on date.
            return servicemen_list

# a = Sql_Database()
# b = Serviceman("Test3", "Test2", "Test2", "Test2")
# a.insert_data(b)
# serviceNumber = "Test3"
# a.drop_data(serviceNumber)

# serviceNumber_input = input("Enter serviceNumber: ")
# found = a.search_database_serviceNumber(serviceNumber_input)
# if found is None:
#     print("Service number entered is not recognised.")
# else:
#     print(found.get_service_number(), found.get_first_name(), found.givenNames, found.get_last_name())
#
# firstName_input = input("Enter firstName: ")
# lastName_input = input("Enter lastName: ")
# list_servicemen = a.search_database_first_last_name(firstName_input, lastName_input)
# if len(list_servicemen) == 0:
#     print("There are zero transactions listed in the database..")
# else:
#     for serviceman in list_servicemen:
#         print(serviceman.get_service_number(), serviceman.get_first_name(), serviceman.get_given_names(), serviceman.get_last_name())
#
# list_servicemen = a.list_all_servicemen()
# if len(list_servicemen) == 0:
#     print("There are zero transactions listed in the database..")
# else:
#     for serviceman in list_servicemen:
#         print(serviceman.get_service_number(), serviceman.get_first_name(), serviceman.get_given_names(), serviceman.get_last_name())
