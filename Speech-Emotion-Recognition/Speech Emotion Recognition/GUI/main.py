import sys
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
#from PyQt5.QtCore import QResource
from func import Clock




app = QGuiApplication(sys.argv)


#QResource.registerResource('resources.rcc')

app.setWindowIcon(QIcon('disc_logo.png'))
clock_work = Clock()

#clock_work.record()
engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty('clock', clock_work)


engine.load('all.qml')
engine.quit.connect(app.quit)

sys.exit(app.exec_())
