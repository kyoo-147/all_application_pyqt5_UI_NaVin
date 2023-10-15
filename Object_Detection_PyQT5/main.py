import re
import sys
from PyQt5.QtWidgets import *
from utils.id import getId, saveId
from loginUI import loginForm
from registerUI import registerForm
from GUI import Ui_MainWindow

# Public password account
class skipWindow:
    windowMain = None
    windowLogin = None
    windowRegister = None
    
# Class này là giao diện login
class windowLogin(QMainWindow):
    def __init__(self, parent = None):
        super(windowLogin, self).__init__(parent)
        self.loginUI = loginForm()
        self.loginUI.setupUi(self)
        self.initSlots()
        # self.hidenPassword()

    def initSlots(self):
        # Using login button and enter key
        self.loginUI.buttonLogin.clicked.connect(self.signIn)
        self.loginUI.editPassword.returnPressed.connect(self.signIn)
        self.loginUI.buttonRegister.clicked.connect(self.createID)

    # Skip to register UI
    def createID(self):
        skipWindow.windowRegister = windowRegister()
        skipWindow.windowRegister.show()

    # This function is to login using login button or press enter
    def signIn(self):
        # Get username and password from login GUI
        username = self.loginUI.editUsername.text().strip()
        password = self.loginUI.editPassword.text().strip()

        # Get information login and password for Login UI 
        USER_PWD = getId()
        # Check username is correct
        if username not in USER_PWD.keys():
            replay = QMessageBox.warning(self, "Failed to login!", "Invalid username!", QMessageBox.Ok)
        else:
            # Check password is correct and skip to GUI
            if USER_PWD.get(username) == password:
                print("\nSkipping to main window\n\n")
                skipWindow.windowMain = Ui_MainWindow()
                skipWindow.windowMain.show()
                self.close()
            # Return if the password is wrong
            else:
                replay = QMessageBox.warning(self, "Failed to login!", "The password is incorrect!", QMessageBox.Ok)

    # The password edit box is hidden, use when .UI did not set up hiden mode
    def hidenPassword(self):
        self.loginUI.editPassword.setEchoMode(QLineEdit.Password)

# Register GUI
class windowRegister(QDialog):
    def __init__(self, parent = None):
        super(windowRegister, self).__init__(parent)
        self.registerUI = registerForm()
        self.registerUI.setupUi(self)
        self.initSlots()

    # Click to register new account or cancel
    def initSlots(self):
        self.registerUI.pushButtonRegister.clicked.connect(self.newAccount)
        self.registerUI.pushButtonCancel.clicked.connect(self.cancel)

    # Create new account
    def newAccount(self):
        # Get username and password from login GUI
        newUsername = self.registerUI.editUsername.text().strip()
        newPassword = self.registerUI.editPassword.text().strip()
        # make a pattern
        pattern = "^[A-Za-z0-9_-]*$"

        # Check username is empty
        if newUsername == "" or newPassword == "":
            replay = QMessageBox.warning(self, "Abort", "Invalid username or password!", QMessageBox.Ok)
        elif bool(re.match(pattern, newUsername)) != True or bool(re.match(pattern, newPassword)) != True:
            replay = QMessageBox.warning(self, "Abort", "Please sure that the syntax is in latin", QMessageBox.Ok)
        else:
            # Check username is exist
            # Get information login and password for Login UI
            USER_PWD = getId()
            if newUsername in USER_PWD.keys():
                replay = QMessageBox.warning(self, "Abort", "Username is exist!", QMessageBox.Ok)
            else:
                # Successful created account
                saveId(newUsername, newPassword)
                replay = QMessageBox.warning(self, "Abort", "Successful!", QMessageBox.Ok)
                self.close()

    def cancel(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Choose Log In GUI is main GUI
    skipWindow.windowLogin = windowLogin()
    skipWindow.windowLogin.show()
    sys.exit(app.exec_())