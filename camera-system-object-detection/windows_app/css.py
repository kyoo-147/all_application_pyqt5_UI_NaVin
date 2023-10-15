backgroundColor = 'rgb(35, 35, 35)'
buttonHoverColor = 'rgb(80, 80, 80)'
buttonPressedColor = 'rgb(110, 110, 110)'
triggerStandardColor = 'rgb(45, 45, 45)'
triggerFiredColor = 'rgb(100, 0, 0)'

windowStyle = '''
    *{
        font-size: 16px;
        font-family: Helvetica, serif;
        color: rgb(235, 235, 235);
    }

    *#window {
        background: ''' + backgroundColor + '''
    }
'''

btnStyle =  '''
    QPushButton {
        width: 85px;
        height: 25px;
        border: none;
        border-bottom: 3px solid rgb(235, 235, 235);
        padding: 5%;
        margin: 0px;
    }
    QPushButton:hover {
        background: ''' + buttonHoverColor + ''';
    }
    QPushButton:pressed {
        background: ''' + buttonPressedColor + ''';
    }
    '''

btnTriggerStyle =  '''
    QPushButton {
        border: 1px solid gray;
        padding: 5%;
        margin: 0px;
    }
    QPushButton:hover {
        background: ''' + buttonHoverColor + ''';
    }
    QPushButton:pressed {
        background: ''' + buttonPressedColor + ''';
    }
    '''

blobSizeTextEdit = '''
    QLineEdit {
        padding: 2px;
        background: black;
    }
'''

imageSettingButton = '''
    QPushButton {
        padding: 0;
        margin: 0px;
    }
    '''

scrollAreaStyle = '''
    QWidget#triggersScrollArea {
        background: ''' + buttonHoverColor + ''';
        color: black;
    }
'''

triggerStandard = '''
    QWidget#triggerBackground {
        background-color: ''' + triggerStandardColor + ''';
        border: 2px inset gray;
    }
    '''

triggerFired = '''
    QWidget#triggerBackground {
        background-color: ''' + triggerFiredColor + ''';
        border: 2px inset red;
    }
    '''

imageStyle = '''
    QWidget {
        border: 1px solid gray;
        margin: 0;
        padding: 0;
    }
'''

title = '''
    * {
        font-weight: bold;
    }
'''

checkBoxStyle = '''
    * {
        image: linear-gradient(black, white);
    }
'''

textBlack = '''
    * {
        color: black;
    }
'''

textGreen = '''
    * {
        color: green;
    }
'''

textRed = '''
    * {
        color: red;
    }
'''