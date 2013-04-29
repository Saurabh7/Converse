
from PySide import QtCore, QtGui

mainProtocols = []

class Ui_MainWindow(object):

    port = 0
    ip = ''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(193, 320)
        MainWindow.setMinimumSize(QtCore.QSize(193, 320))
        MainWindow.setMaximumSize(QtCore.QSize(193, 320))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 10, 193, 306))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setMinimumSize(QtCore.QSize(191, 271))
        self.textEdit.setMaximumSize(QtCore.QSize(191, 271))
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(191, 27))
        self.lineEdit.setMaximumSize(QtCore.QSize(191, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.addInput)
        
        self.verticalLayout.addWidget(self.lineEdit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def addInput(self):
	#skip empty text
	if self.lineEdit.text() and port:
	    message = self.lineEdit.text()
            mainProtocols[0].sendMessage(message)

	self.lineEdit.clear()


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Chat Window", None, QtGui.QApplication.UnicodeUTF8))


class controlChat(QtGui.QMainWindow):
    def __init__(self,ip,port,userName, protocol,parent=None):
	super(controlChat, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.port = port
        self.ui.ip = ip
        self.userName = userName
        mainProtocols.append(protocol)
        self.ui.setupUi(self)

