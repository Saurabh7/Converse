"""
Graph implemenation shown in ui as listView
"""

from PySide import QtCore, QtGui
from PySide.QtCore import *
import sys
from Graph import *     # import graph

user_graph = main()

class listmodel(QtCore.QAbstractListModel):
    def __init__(self,mlist,parent=None):
	super(listmodel, self).__init__(parent)
	self.items = mlist

    def rowCount ( self, parent = QModelIndex):
	return len(self.items)

    def data(self, index, role = Qt.DisplayRole):
	if role == Qt.DisplayRole:
	# The view is asking for the actual data, so, just return the item it's asking for.
	    return self.items[index.row()]

    def addItem(self, item):
  	self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
  	self.items.append(str(item))
  	self.endInsertRows()

    def remItem(self, item):
	self.beginRemoveRows(QModelIndex(), len(self.items) ,len(self.items))
	self.items.remove(str(item))
	self.endRemoveRows()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(195, 347)
        MainWindow.setMinimumSize(QtCore.QSize(195, 347))
        MainWindow.setMaximumSize(QtCore.QSize(195, 347))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
	self.listView = QtGui.QListView(self.centralwidget)
    
	self.listView.setMinimumSize(QtCore.QSize(181, 271))
        self.listView.setMaximumSize(QtCore.QSize(181, 271))
        self.listView.setObjectName("listView")
	
	user_list = user_graph.get_users()      #load graph
	self.model = listmodel(user_list)
	self.listView.setModel(self.model)
	
        
	self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
	self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
	self.pushButton.clicked.connect(self.chat)        

	self.horizontalLayout.addWidget(self.pushButton)
        
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
	self.pushButton_2.clicked.connect(self.rem)        
        
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 195, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))

    def chat(self):
	pass

    def rem(self):
        item =  self.listView.selectedIndexes()
        itemText = str(item[0].data())
        if itemText and (itemText in self.model.items):
            #user_graph.remove(itemText)
            self.model.remItem(itemText)
            for user in user_graph.root.findall('user') :
                idu = user.get('id')
                if idu == itemText :
                    user_graph.root.remove(user)
                    user_graph.tree.write("users.xml")


class ControlMainWindow2(QtGui.QMainWindow):
    def __init__(self, parent=None):
	super(ControlMainWindow2, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = ControlMainWindow2()
    mw.show()
    sys.exit(app.exec_())

