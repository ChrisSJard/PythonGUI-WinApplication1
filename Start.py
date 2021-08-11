from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QColor, QPixmap, QCursor
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import *
import sys
import os
from SingleWindow import *
from MultipleWindow import *
import resource

class StartupWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Test Windows Application")
        self.setGeometry(50,50,800,400)
        self.setWindowIcon(QIcon(':/resources/DesktopICon.ico'))
       
        self.setStyleSheet("background-color: #176363;")
        grid = QGridLayout()
        ''' Buttons '''
        SingleButton = QPushButton(self)
        SingleButton.setText("Single Analysis")
        SingleButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        MultipleButton = QPushButton(self)
        MultipleButton.setText("Multiple Analysis")
        MultipleButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        grid.addWidget(SingleButton,0,0)
        grid.addWidget(MultipleButton,0,1)
        '''Events '''
        SingleButton.clicked.connect(self.SingleButton_clicked)
        MultipleButton.clicked.connect(self.MultipleButton_clicked)
        '''Styling '''
        SingleButton.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
        MultipleButton.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred)
        SingleButton.setStyleSheet('''QPushButton{color:#fff;
                                                  font: bold 21px;
                                                  text-align: bottom right;
                                                  padding:10px;
                                                  border-image: url(:/resources/singleshot.jpg);
                                                  border-radius:20px;
                                                 }
                                      QPushButton:hover {
                                                  color: #8ffff4;
                                                 }'''
                                   )
        MultipleButton.setStyleSheet('''QPushButton{color:#fff;
                                                    font: bold 21px;
                                                    text-align: bottom right;
                                                    padding:10px;
                                                    border-image: url(:/resources/multiple.jpg);border-radius:20px;
                                                   }
                                        QPushButton:hover {
                                                    color: #8ffff4;
                                                   }'''
                                    )
        self.setLayout(grid)

    def SingleButton_clicked(self):
        win = SingleWindow(self)
        win.show()

    def MultipleButton_clicked(self):
        win = MultipleWindow(self)
        win.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StartupWindow()
    win.show()
    sys.exit(app.exec_())
