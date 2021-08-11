from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QColor, QPixmap, QCursor, QPalette, QLinearGradient, QBrush, QPainter
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import *
from numpy import append
from libMap.Preprocessing import *
from libMap.PeakFinding import *
from libMap.Analysis import *
from libMap.AlgorithmSingle import *
from libMap.Exporter import *
import time
import os
import xlsxwriter
import datetime
from datetime import datetime
import csv

class ProgressWindow(QMainWindow):
    def __init__(self ,parent):
        super().__init__(parent)
        windowpanel = QWidget()
        self.idxList = []
        self.filenameList = []
        self.QCResultList = []
        ''' Add new features to list'''
        self.alphaGlycateList = []
        self.alphaGlycateRatioList = []
        self.alphaGlycateProbList = []
        self.alphaGlycateAbsoluteList =[]
        self.resultList = []
        self.OldalphaGlycateRatioList = []
        self.OldalphaGlycateProbList = []
        self.alphaPeakList = []
        self.setWindowTitle("Loading Data")
        self.setGeometry(50,50,400,100)
        grid = QGridLayout()
        self.setStyleSheet("QMainWindow{background-color: white;}")
        self.setStyleSheet("QWidget{background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.5 #ffffff, stop: 1.0 #176363);}")
        self.__label1 = QLabel("Progress Status")
        self.__label1.setStyleSheet('''QLabel{background-color: transparent} ''')
        self.__label2 = QProgressBar(self)
        grid.addWidget(self.__label1, 0,0)
        grid.addWidget(self.__label2,0,1)
        windowpanel.setLayout(grid)
        self.setCentralWidget(windowpanel)
        self.show()

    def ThreadStart(self, path,threshold1, threshold2, threshold3, threshold4, smootherType):
        self.__savelocation = path
        self.Th = AlgorithmThread(path,threshold1, threshold2, threshold3, threshold4,
                                  smootherType,self.idxList,self.filenameList, self.QCResultList,
                                  self.alphaGlycateList,self.alphaGlycateRatioList,
                                  self.alphaGlycateProbList,self.alphaGlycateAbsoluteList,
                                  self.resultList,self.OldalphaGlycateRatioList, 
                                  self.OldalphaGlycateProbList, self.alphaPeakList)
        self.Th.ProgressbarChanged.connect(self.UpdateProgress)
        self.Th.start()

    def UpdateProgress(self, val):
        self.__label2.setValue(val)
        if val == 100:
            self.close()
            try:
                excelExport(self.__savelocation,self.filenameList, self.resultList, self.alphaGlycateList, 
                            self.alphaGlycateRatioList,self.alphaGlycateProbList, self.alphaGlycateAbsoluteList,
                            self.OldalphaGlycateRatioList,self.OldalphaGlycateProbList, self.alphaPeakList,
                           )
                WarningMessage = QMessageBox()
                WarningMessage.setStyleSheet('''background-color: white''')
                WarningMessage.setIcon(QMessageBox.Information)
                WarningMessage.setWindowTitle('Status')
                WarningMessage.setText("Completed!")
                WarningMessage.setStandardButtons(QMessageBox.Ok)
                WarningMessage.show()
                WarningMessage.exec_()
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
            
class AlgorithmThread(QThread):
    ProgressbarChanged = pyqtSignal(int)
    def __init__(self, path,threshold1, threshold2, threshold3, threshold4, smootherType,
                 idxList,filenameList, QCResultList,alphaGlycateList,alphaGlycateRatioList,alphaGlycateProbList,
                 alphaGlycateAbsoluteList,resultList,OldalphaGlycateRatioList,OldalphaGlycateProbList,alphaPeakList,parent = None):
        super().__init__(parent)
        self.path = path
        self.__thres = self.switchCaseThreshold(threshold1, threshold2, threshold3, threshold4)
        self.idxList = idxList
        self.filenameList = filenameList
        self.QCResultList = QCResultList
        self.alphaGlycateList = alphaGlycateList
        self.alphaGlycateRatioList = alphaGlycateRatioList
        self.alphaGlycateProbList = alphaGlycateProbList
        self.alphaGlycateAbsoluteList = alphaGlycateAbsoluteList
        self.OldalphaGlycateRatioList = OldalphaGlycateRatioList
        self.OldalphaGlycateProbList = OldalphaGlycateProbList
        self.alphaPeakList = alphaPeakList
        self.resultList = resultList
        
    def run(self):
        self.__count = 0
        idx = 0
        '''adjust later to take actual input for fresh or bloddcard'''
        FILES = os.listdir(self.path)
        FolderSize = len(FILES)
        progress = float(100/FolderSize)
        progressUpdate = 0
        while self.__count <FolderSize:
            for filename in FILES:
                if filename.split(".")[-1] == "mzml" or filename.split(".")[-1] == "txt":
                    path = self.path + "/" + filename
                    Decoder = DecoderNew(path,7200, 8500)
                    SmoothInt = Smoothing(Decoder.get_Int(), windowsize=9, cycle=5)
                    baseline = Baseline(SmoothInt.get_x(), 10000000000000, 0.01)
                    Smoother = SmoothInt.get_x() - baseline.get_baseline()
                    PeakDet = PeakDetection(Smoother, prom=self.__thres)
                    PeakExt = PeakExtraction(Decoder.get_mz(), Smoother, PeakDet.get_Peaks() )
                    ValleyExt = ValleyExtraction(Decoder.get_mz(), Smoother, PeakDet.get_Valleys() )
                    DataExt = BestPeakEstimator(Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList(),PeakDet.get_Prominence(), PeakDet.get_Widths() )        
                    self.__Alphadata = DataExt.get_AlphaData()
                    self.__Betadata = DataExt.get_BetaData()
                    self.__alphaMatrixdata = DataExt.get_alphaMatrixData()
                    self.__betaMatrixdata = DataExt.get_betaMatrixData()
                    '''QC CheckPeakFound of Alpha, Beta and CheckMatrixs (smoothmight be best)'''
                    if DataExt.get_AlphaData()[0] != 0 or DataExt.get_BetaData()[0] != 0:
                        PeakDistExt = GlycatedEstimator(DataExt.get_AlphaData(), Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList(),PeakDet.get_Prominence(), PeakDet.get_Widths())
                        RefValley = MinValleyEstimator(DataExt.get_AlphaData(), Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList())
                        '''QC CheckPeakFound '''
                        self.__alphaGlydata = PeakDistExt.get_alphaGlyData()
                        self.__minValleydata = RefValley.get_x()
                        if PeakDistExt.get_alphaGlyData()[0] != 0:
                            outComes = DataAnalysis(DataExt.get_AlphaData()[1],DataExt.get_BetaData()[1],PeakDistExt.get_alphaGlyData()[2],DataExt.get_alphaMatrixData()[1],DataExt.get_betaMatrixData()[1], RefValley.get_x(),PeakDistExt.get_alphaGlyData()[1])
                            self.__RatioCalaculationdata = [outComes.get_alphaRatio(),outComes.get_betaRatio(),outComes.get_glyAlphaRatio(),outComes.get_alphaMatrixRatio(),outComes.get_betaMatrixRatio(), outComes.get_oldglyAlphaRatio()]
                            self.__ProbOutcomesdata = [outComes.get_alphaThalassemiaProb(),outComes.get_betaThalassemiaProb(),outComes.get_diabetesProb(),outComes.get_olddiabetesProb()]
                            self.__resultString = outComes.get_strResult()
                            #remove below for mike version
                            #self.QCResultList.append("Pass")
                            self.__QcResult = "Pass"
                        else:
                            self.__RatioCalaculationdata = [None,None,None,None, None, None]
                            self.__ProbOutcomesdata = [None,None,None, None]     
                            self.__resultString = ["Fail", "Fail", "Fail"]
                             #remove below for mike version
                            #self.QCResultList.append("HbA1C Fail")
                            self.__QcResult = "HbA1C Fail"
                    else:
                        ''' Need to handle for when Alpha and Beta Not found'''
                        self.__alphaGlydata = [0, 0, 0, 0]
                        self.__RatioCalaculationdata = [None,None,None,None, None, None]
                        self.__ProbOutcomesdata = [None,None,None, None]     
                        self.__resultString = ["QcFail", "QcFail", "QcFail"]
                        #remove below for mike version
                        #self.QCResultList.append("Fail")
                        self.__QcResult = "QcFail"
                        pass
                    self.__count += 1.0
                    progressUpdate += progress
                    self.ProgressbarChanged.emit(progressUpdate)
                    #remove below for mike version
                    self.idxList.append(idx)
                    #remove below for mike version
                    self.filenameList.append(filename)
                    #remove below for mike version
                    self.alphaGlycateList.append(self.__alphaGlydata[2])
                    self.alphaGlycateAbsoluteList.append(self.__alphaGlydata[1])
                    self.__HbA1cRegion = self.__alphaGlydata[0]
                    self.__HbA1cAbsolute = self.__alphaGlydata[1]
                    self.__HbA1cReading = self.__alphaGlydata[2]
                    #remove below for mike version
                    self.alphaGlycateRatioList.append(self.__RatioCalaculationdata[2])
                    self.__HbA1cRatio = self.__RatioCalaculationdata[2]
                    #remove below for mike version
                    self.resultList.append(self.__resultString[2])
                    self.alphaGlycateProbList.append(self.__ProbOutcomesdata[2])
                    self.__HbA1cProbability = self.__ProbOutcomesdata[2]
                    self.__Hbresult = self.__resultString[2]

                    self.OldalphaGlycateRatioList.append(self.__RatioCalaculationdata[5])
                    self.OldalphaGlycateProbList.append(self.__ProbOutcomesdata[3])
                    self.__alphaPeak = DataExt.get_AlphaData()[1]
                    self.alphaPeakList.append(DataExt.get_AlphaData()[1])

                    csvExport(path,self.__Hbresult,self.__QcResult,
                              self.__HbA1cRegion,self.__HbA1cReading,
                              self.__HbA1cRatio, self.__HbA1cAbsolute,self.__HbA1cProbability,
                              self.__RatioCalaculationdata[5], self.__ProbOutcomesdata[3], self.__alphaPeak
                             )
                    idx += 1
                    #print ("##################################")
                    #print ("New added Count = ", self.__count )
                    #print ("##################################")
                else:
                    self.__count += 1.0
                    progressUpdate += progress
                    self.ProgressbarChanged.emit(progressUpdate)
        if progressUpdate < 100:
            progressUpdate = 100
            self.ProgressbarChanged.emit(progressUpdate)

    def switchCaseThreshold(self, tr1, tr2, tr3, tr4):
        if tr1 == True:
            return (0.01)
        elif tr2 == True:
            return (0.1)
        elif tr3 == True:
            return (0.5)
        elif tr4 == True:
            return (1.0)
        else:
            return 0.01
