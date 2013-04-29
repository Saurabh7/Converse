"""
Main client
"""

from PySide import QtCore, QtGui
import sys
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
#from twisted.internet import qtreactor
import qt4reactor
from chat import controlChat as chatWindow

#get the graph implementation
from userGraph import *


graphOpened = 0
connected = 0
userName = ''
chatList = []
talkingTo = ''
protocolList= []
mainProtocols = []

class Ui_MainWindow(QtGui.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(195, 347)
        MainWindow.setMinimumSize(QtCore.QSize(195, 347))
        MainWindow.setMaximumSize(QtCore.QSize(195, 347))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 10, 193, 286))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
	self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setMinimumSize(QtCore.QSize(191, 251))
        self.textEdit.setMaximumSize(QtCore.QSize(191, 251))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
	self.verticalLayout.addWidget(self.textEdit)
        self.textEdit.append("Please set your user Name")
        
	self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(191, 27))
        self.lineEdit.setMaximumSize(QtCore.QSize(191, 27))
        #Enter press signal
	self.lineEdit.returnPressed.connect(self.addInput)
	self.lineEdit.setObjectName("lineEdit")
        
	self.verticalLayout.addWidget(self.lineEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 195, 25))
        self.menubar.setObjectName("menubar")
        self.menuConnect = QtGui.QMenu(self.menubar)
        self.menuConnect.setObjectName("menuConnect")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #connect to new 
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.triggered.connect(self.getPort)
	
        #open previous connected
        self.actionNames = QtGui.QAction(MainWindow)
        self.actionNames.setObjectName("actionNames")
        self.actionNames.triggered.connect(self.getNames)

        self.actionuserName = QtGui.QAction(MainWindow)
        self.actionuserName.setObjectName("actionuserName")
        self.actionuserName.triggered.connect(self.setUserName)

	self.menuConnect.addAction(self.actionConnect)
        self.menuConnect.addAction(self.actionNames)
        self.menuConnect.addAction(self.actionuserName)
        self.menubar.addAction(self.menuConnect.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #Get ip address entered
    def getPort(self):                                         
	address, ok = QtGui.QInputDialog.getText(self , 'ConverseConnect','Enter IP:PORT :')
        global connected
	if ok and not connected:
	    ip=str(address)
	    ip1=ip.split(':',1)
	    ipAddress = ip1[0]
	    ipPort = int(ip1[1])
            reactor.connectTCP(ipAddress, ipPort, factory)
            print mainProtocols
            
	    print ipAddress+'>>>'+str(ipPort)   
        
        #open a new window for new chat.
        elif connected :
            ip=str(address)
            ip1=ip.split(':',1)
	    ipAddress = ip1[0]
	    ipPort = int(ip1[1])
            reactor.connectTCP(ipAddress, ipPort, factory)
            length = len(protocolList)
            newProtocol = protocolList[length-1]
            chat = chatWindow(ipAddress, ipPort, userName, newProtocol, self)
            chat.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            chatList.append(chat)
            chat.show()


    #Graphed list of previous users.
    def getNames(self):
        if not graphOpened : 
            graphNames = ControlMainWindow2(self)
            graphNames.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            graphNames.show()
    #set user name
    def setUserName(self):
	global userName
        user_Name, ok = QtGui.QInputDialog.getText(self , 'User Name','Enter User Name :')
        userName = str(user_Name)
    
    def addInput(self):
	#skip empty text
	global port , userName, connected
	if self.lineEdit.text() and connected and userName:
	    message = self.lineEdit.text()
            mainProtocols[0].sendMessage(message)

	self.lineEdit.clear()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Converse", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConnect.setTitle(QtGui.QApplication.translate("MainWindow", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNames.setText(QtGui.QApplication.translate("MainWindow", "Names", None, QtGui.QApplication.UnicodeUTF8))
        self.actionuserName.setText(QtGui.QApplication.translate("MainWindow", "Set Name", None, QtGui.QApplication.UnicodeUTF8))


# send and receive message
class Chatty(LineReceiver):
    # send message
    def sendMessage(self, msg):
	msg1 = userName + '>' + msg
        self.sendLine(msg1.encode('utf-8'))
        mw.ui.textEdit.append(userName + ':' + msg )
    
    # receive message
    def lineReceived(self, data):
	global talkingTo
        global connected
        connected = 1
        data=data.decode('utf-8')
        message=str(data)
        full_msg = message.split('>' , 1)
        talkingTo = full_msg[0]
        msg=full_msg[1]
        mw.ui.textEdit.append(talkingTo +':' + msg  )

    def connectionMade(self):
	print 'made connection'
        global connected
        if not connected:
            mainProtocols.append(self)
        connected = 1
        #maintain a list of protocols to handle connections
        protocolList.append(self)
        print protocolList

    def connectionLost(self):
        protocolList.remove(self)

ChattyFactory = protocol.ServerFactory()
ChattyFactory.protocol = Chatty
factory = protocol.ClientFactory()
factory.protocol = Chatty


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
	super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        
   
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    #Installing the qtreactor 
    
    qt4reactor.install()
    from twisted.internet import reactor
    
    try:
        reactor.listenTCP(1500,ChattyFactory)
    except:
        reactor.listenTCP(1501,ChattyFactory)
    reactor.runReturn()
    mw = ControlMainWindow()
    mw.show()
    sys.exit(app.exec_())

