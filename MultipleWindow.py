from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QColor, QPixmap, QCursor, QPalette, QLinearGradient, QBrush, QPainter
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import *
import os
import sys
from libMap.MultipleWindowOutput import *

class MultipleWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        windowpanel = QWidget()
        self.setWindowTitle("Test Windows Application - Multiple Analysis")
        self.setGeometry(50,50,800,410)
        self.setStyleSheet("QWidget{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.5 #ffffff, stop: 1.0 #176363);}")
        grid = QGridLayout()
        ''' Widgets and options'''
        textLabel1 = QLabel()
        textLabel2 = QLabel()
        self.textLabel4 = QLineEdit()
        self.textLabel4.setText("...Specify Folder Location")
        textLabel5 = QPushButton()
        textLabel5.setText("Select Folder")
        #------------------------------------------------------------------------------------------------
        textLabel6 = QGroupBox("Threshold Limits")
        vbox = QVBoxLayout()
        textLabel6.setLayout(vbox)
        self.__threshold1 = QRadioButton("0.01")
        self.__threshold1.setChecked(True)
        vbox.addWidget(self.__threshold1)
        self.__threshold2 = QRadioButton("0.1")
        vbox.addWidget(self.__threshold2)
        self.__threshold3 = QRadioButton("0.5")
        vbox.addWidget(self.__threshold3)
        self.__threshold4 = QRadioButton("1.0")
        vbox.addWidget(self.__threshold4)
        #------------------------------------------------------------------------------------------------
        textLabel7 = QGroupBox("Smoothing Settings")
        vbox2 = QVBoxLayout()
        textLabel7.setLayout(vbox2)
        self.Type1 = QRadioButton("Low Smoothing")
        vbox2.addWidget(self.Type1)
        self.Type2 = QRadioButton("High Smoothing")
        self.Type2.setChecked(True)
        vbox2.addWidget(self.Type2)
        #------------------------------------------------------------------------------------------------

        self.textLabel9 = QPushButton()
        self.textLabel9.setText("RUN")
        self.textLabel3 = DragandDrop("Drag and Drop File",threshold1 =self.__threshold1, threshold2 =self.__threshold2, threshold3 =self.__threshold3, threshold4 =self.__threshold4,smootherType= self.Type2,parent =self)
        grid.addWidget(textLabel1,0,0)  #maplogo
        grid.addWidget(textLabel2,0,1,1,3) #spectra image
        grid.addWidget(self.textLabel3,1,0,2,2) # drag and drop
        grid.addWidget(self.textLabel4,1,2,1,2, Qt.AlignVCenter) #file textpath
        grid.addWidget(textLabel5,2,2, Qt.AlignLeft|Qt.AlignTop) #find path button
        grid.addWidget(textLabel6,3,0) #groupbox kit tests
        grid.addWidget(textLabel7,3,1) #groupbox blood type
        #grid.addWidget(textLabel8,3,2)  #groupbox status checkers
        grid.addWidget(self.textLabel9,3,3, Qt.AlignCenter)  # run button
        '''Events'''
        textLabel5.clicked.connect(self.textLabel5_clicked)
        self.textLabel9.clicked.connect(self.textLabel9_clicked)
        self.textLabel9.setEnabled(False)
        '''Styling '''
        textLabel1.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        textLabel2.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.textLabel3.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.textLabel4.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        textLabel5.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)
        textLabel6.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        textLabel7.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.textLabel9.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        textLabel1.setStyleSheet('''QLabel{image: url(":/resources/logo.jpg"); background-color:transparent;}''')
        self.textLabel3.setStyleSheet('''background-color: transparent;border: 2px dashed #020745;font: 16px bold "Franklin Gothic Medium";color:#bdb3a7;''')
        textLabel2.setStyleSheet('''QLabel{border-image: url(":/resources/Spectra_SHot2.jpg")}''')
        self.textLabel4.setStyleSheet(''' Margin: 0px 50px 0px 0px;Padding:5px;Color: #FF767171;background-color:#FFE2E2E2''')  #top right bottom left
        textLabel5.setStyleSheet('''QPushButton{Padding:5px 5px 5px 10px;
                                                border:4px solid #FF176363;
                                                border-radius:5px;
                                                background-color:#FF4DA6A6;
                                                Color: white;
                                                Font: bold 16px
                                               }
                                    QPushButton:hover{background-color:#8ffff4;}
                                ''')
        textLabel6.setStyleSheet('''QGroupBox{padding:4px;background-color: transparent; border:3px solid #FFFFFF;border-radius:20px; font: bold}''')
        textLabel7.setStyleSheet('''QGroupBox{padding:4px;background-color: transparent; border:3px solid #FFFFFF;border-radius:20px; font: bold}''')
        #textLabel8.setStyleSheet('''QGroupBox{padding:4px;background-color: transparent; border:3px solid #FFFFFF;border-radius:20px; font: bold}''')
        self.textLabel9.setStyleSheet('''QPushButton{Padding:5px 20px 5px 20px;
                                                border:4px solid #4d4d4d;
                                                border-radius:5px;
                                                background-color:#cfcfcf;
                                                Color: black;
                                                Font: bold 16px
                                               }
                                    ''')
        self.__threshold1.setStyleSheet('''background-color: transparent ''')
        self.__threshold2.setStyleSheet('''background-color: transparent ''')
        self.__threshold3.setStyleSheet('''background-color: transparent ''')
        self.__threshold4.setStyleSheet('''background-color: transparent ''')

        self.Type1.setStyleSheet('''background-color: transparent ''')
        self.Type2.setStyleSheet('''background-color: transparent ''')

        windowpanel.setLayout(grid)
        self.setCentralWidget(windowpanel)

    def textLabel5_clicked(self):
        '''File Handler'''
        dialog = QFileDialog.Options()
        folderName= QFileDialog.getExistingDirectory(self,"Select Folder", "c:\\ ", options= dialog)
        try:
            '''FileHandler Class Operation'''
            if len(folderName) > 0 :
                self.textLabel4.setText(folderName)
                self.textLabel9.setEnabled(True)
                self.textLabel9.setStyleSheet('''QPushButton{Padding:5px 20px 5px 20px;
                                                    border:4px solid #FF176363;
                                                    border-radius:5px;
                                                    background-color:#FF4DA6A6;
                                                    Color: white;
                                                    Font: bold 16px
                                                   }
                                                    QPushButton:hover{background-color:#8ffff4;}
                                                ''')
            else:
                pass
        except:
            error = sys.exc_info()
            self.textLabel4.setText(self.textLabel4.text())

    def textLabel9_clicked(self):
        ''' RUN Analysis '''
        try:
            win = ProgressWindow(self)
            win.ThreadStart( path = self.textLabel4.text(),threshold1 =self.__threshold1.isChecked(), threshold2 =self.__threshold2.isChecked(),threshold3 =self.__threshold3.isChecked(),threshold4 =self.__threshold4.isChecked(),smootherType =self.Type2.isChecked())
        except:
                error = sys.exc_info()[0]
                WarningMessageinfo = QMessageBox()
                WarningMessageinfo.setStyleSheet('''background-color: white''')
                WarningMessageinfo.setIcon(QMessageBox.Warning)
                WarningMessageinfo.setWindowTitle('Error')
                WarningMessageinfo.setText("Error occurred to Process File!" )
                WarningMessageinfo.setStandardButtons(QMessageBox.Ok)
                WarningMessageinfo.show()
                WarningMessageinfo.exec_()

class DragandDrop(QPushButton):
    def __init__(self, title, threshold1, threshold2, threshold3, threshold4, smootherType, parent):
        super().__init__(title, parent)
        self.__title = title
        self.__threshold1 = threshold1
        self.__threshold2 = threshold2
        self.__threshold3 = threshold3
        self.__threshold4 = threshold4
        self.__smootherType = smootherType
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet('''QPushButton{image: url(:/resources/filestored32.jpg);background-color: transparent;border: 2px dashed #020745;font: 16px bold "Franklin Gothic Medium";color:#bdb3a7;}''')
            self.setText("\n\n\n\nProcess Folder")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
            self.setStyleSheet('''QPushButton{background-color: transparent;border: 2px dashed #020745;font: 16px bold "Franklin Gothic Medium";color:#bdb3a7;}''')
            self.setText(self.__title)

    def dropEvent(self, e):
        try:
            data = e.mimeData()
            urls = data.urls()
            urls and urls[0].scheme() == 'file'
            folderName = str(urls[0].path())[1:]
            if os.path.isdir(folderName) == True:
                win = ProgressWindow(self)
                win.ThreadStart(path= folderName , threshold1 = self.__threshold1.isChecked(), threshold2 =self.__threshold2.isChecked(), threshold3 = self.__threshold3.isChecked(), threshold4 =self.__threshold4.isChecked(),smootherType = self.__smootherType.isChecked())
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Error: Invalid Folder ")
                dialog.setText("Invalid Folder Type")
                dialog.setIcon(QMessageBox.Warning)
                dialog.exec_()
        except:
            error = sys.exc_info()[0]
            WarningMessage = QMessageBox()
            WarningMessage.setStyleSheet('''background-color: white''')
            WarningMessage.setIcon(QMessageBox.Warning)
            WarningMessage.setWindowTitle('Error')
            WarningMessage.setText("Error occurred to Process File!\n"+str(error) )
            WarningMessage.setStandardButtons(QMessageBox.Ok)
            WarningMessage.show()
            WarningMessage.exec_()
