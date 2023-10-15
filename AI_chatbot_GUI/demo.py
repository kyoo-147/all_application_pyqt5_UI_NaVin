import sys
import openai
import api
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextBrowser, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class ChatBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 250)
        self.setWindowTitle("AI Chatbot")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #303030; color: white;")

        # Create a QVBoxLayout object to manage the widgets in a vertical layout.
        layout = QVBoxLayout()
        # Set the spacing between widgets to 12 pixels.
        layout.setSpacing(12)

        # Create a QLineEdit widget for the user to enter a question.
        self.enterQuestion = QLineEdit()
        # Set the style and placeholder text for the QLineEdit widget.
        self.enterQuestion.setStyleSheet('font-size: 12px; height: 30px; border: 2px solid #343434')
        self.enterQuestion.setPlaceholderText("Enter question here...")
        # Add the QLineEdit widget to the layout.
        layout.addWidget(self.enterQuestion)

        # Create a QPushButton widget for the user to submit their question.
        self.button = QPushButton("SUBMIT", clicked=self.generateContent)
        # Set the size and style of the button.
        self.button.setFixedSize(478, 30)
        self.button.setStyleSheet("background-color: #343434; color: white; border-radius: 2px;")
        # Add the button to the layout.
        layout.addWidget(self.button)

        # Create an icon widget for the AI logo.
        self.logo = QTextBrowser()
        # Set the size and style of the AI logo.
        self.logo.insertHtml('<div style="text-align: center;"><a href="https://openai.com"><img src="icon.png" width="18" height="18"></a></div>')
        self.logo.setStyleSheet("border: none;")
        # Set the openLinks property to False.
        self.logo.setOpenLinks(False)
        # Connect the anchorClicked signal to the open_website slot function.
        self.logo.anchorClicked.connect(self.open_website)
        # Add the AI logo to the layout.
        layout.addWidget(self.logo)

        # Create a QTextBrowser widget to display the Chatbot replies.
        self.textBrowser = QTextBrowser()
        # Set the style of the QTextBrowser widget.
        self.textBrowser.setStyleSheet("font-size: 11px; border: none;")
        # Add the QTextBrowser widget to the layout.
        layout.addWidget(self.textBrowser)

        # Set the layout of the ChatBot window.
        self.setLayout(layout)

        # Connect the textChanged signal to the enableButton slot.
        self.enterQuestion.textChanged.connect(self.enableButton)

        # Set the button to be disabled initially.
        self.button.setEnabled(False)

    # Enables or disables the chat button based on the presence of text in the enterQuestion field.
    def enableButton(self):
        if bool(self.enterQuestion.text()):
            # Enable the button, set the color and set the cursor to a pointing hand.
            self.button.setEnabled(True)
            self.enterQuestion.setStyleSheet('font-size: 12px; height: 30px; border: 2px solid #282828')
            self.button.setStyleSheet("background-color: #282828; color: white; border-radius: 2px;")
            self.button.setCursor(Qt.PointingHandCursor)
        else:
            # Disable the button, set the color and set the cursor back to the default arrow cursor.
            self.button.setEnabled(False)
            self.enterQuestion.setStyleSheet('font-size: 12px; height: 30px; border: 2px solid #343434')
            self.button.setStyleSheet("background-color: #343434; color: white; border-radius: 2px;")
            self.button.setCursor(Qt.ArrowCursor)

    # Generates Chatbot replies using the OpenAI API.        
    def generateContent(self):
        self.button.setCursor(Qt.WaitCursor) # Adds a loading cursor while waiting for response.
        new_api_key = api.API_KEY
        def chat(prompt):
            completions = openai.Completion.create(model = "text-davinci-003", prompt = prompt, max_tokens = 1024, api_key = new_api_key)
            message = completions.choices[0].text
            return message
        humanQuestion = self.enterQuestion.text()
        aiReply = chat(humanQuestion)

        # Clear the enterQuestion text field.
        self.enterQuestion.clear()
        # Clear the previous text browser response.
        self.textBrowser.clear()

        # Append the AI response to the text browser.
        self.textBrowser.insertHtml('<div style="text-align: center;">{}</div>'.format(aiReply))

    def open_website(self, url):
        # Open the website in the default web browser when the AI logo is clicked.
        QDesktopServices.openUrl(QUrl(url))

# Set up the Chatbot program using PyQt5.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ChatBot()
    demo.show()
    sys.exit(app.exec_())