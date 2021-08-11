#from threading import Thread
from libMap.Preprocessing import *
from libMap.PeakFinding import *
from libMap.Analysis import *
#delete
#import matplotlib.pyplot as plt
#from peakutils.plot import plot as pplot

class Algorithm():
    def __init__(self, path,threshold1, threshold2, threshold3, threshold4, smootherType):
        #Thread.__init__(self)
        self.__path = path
        self.__thres = self.switchCaseThreshold(threshold1, threshold2, threshold3, threshold4)
        self.start()

    def get_dataMz(self):
        return self.__datax

    def get_dataInt(self):
        return self.__datay

    def get_Alphadata(self):
        return self.__Alphadata

    def get_Betadata(self):
        return self.__Betadata

    def get_alphaMatrixdata(self):
        return self.__alphaMatrixdata

    def get_betaMatrixdata(self):
        return self.__betaMatrixdata

    def get_HaeDistdata(self):
        return self.__HaeDistdata

    def get_AlphaMutation(self):
        return self.__AlphaMutation

    def get_BetaMutation(self):
        return self.__BetaMutation

    def get_alphaGlydata(self):
        return self.__alphaGlydata

    def get_MinValley(self):
        return self.__minValleydata

    def get_RatioCalaculationDistdata(self):
        return self.__RatioCalaculationdata

    def get_ProbOutcomesdata(self):
        return self.__ProbOutcomesdata

    def get_stringResultOutcomes(self):
        return self.__resultString

    def get_QCResultData(self):
        return self.__QcResult

    def start(self):
        Decoder = DecoderNew(self.__path,0, 300)
        #self.__datax = Decoder.get_mz()
        #self.__datay = Decoder.get_Int()
        # Class (Preprocessing)
        SmoothInt = Smoothing(Decoder.get_Int(), windowsize=9, cycle=5)
        baseline = Baseline(SmoothInt.get_x(), 10000000000000, 0.01)
        Smoother = SmoothInt.get_x() - baseline.get_baseline()
        # Class (Peakfinding)
        PeakDet = PeakDetection(Smoother, prom=self.__thres)
        # Class (Peakfinding)
        PeakExt = PeakExtraction(Decoder.get_mz(), Smoother, PeakDet.get_Peaks() )
        # Class (Peakfinding)
        ValleyExt = ValleyExtraction(Decoder.get_mz(), Smoother, PeakDet.get_Valleys() )
        # Class (Peakfinding)
        DataExt = BestPeakEstimator(Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList(),PeakDet.get_Prominence(), PeakDet.get_Widths() )
        self.__Alphadata = DataExt.get_AlphaData()
        self.__Betadata = DataExt.get_BetaData()
        self.__alphaMatrixdata = DataExt.get_alphaMatrixData()
        self.__betaMatrixdata = DataExt.get_betaMatrixData()
        '''QC CheckPeakFound of Alpha, Beta and CheckMatrixs (smoothmight be best)'''
        if DataExt.get_AlphaData()[0] != 0 or DataExt.get_BetaData()[0] != 0:
            # Class (Analysis) get haem distance
            #HaemExt = Haemoglobinopathies(DataExt.get_AlphaData(), DataExt.get_BetaData(), self.__path,self.__check)
            #self.__HaeDistdata = HaemExt.get_HaeDist()
            #self.__AlphaMutation = HaemExt.get_AlphaMutation()
            #self.__BetaMutation = HaemExt.get_BetaMutation()
            # Class (Analysis) get peak by checking for peak distance away from alpha
            PeakDistExt = GlycatedEstimator(DataExt.get_AlphaData(), Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList(),PeakDet.get_Prominence(), PeakDet.get_Widths())
            RefValley = MinValleyEstimator(DataExt.get_AlphaData(), Decoder.get_mz(), PeakExt.get_PeakMzList(), PeakExt.get_PeakIntList(), ValleyExt.get_ValleyMzList(),ValleyExt.get_ValleyIntList())        
            self.__alphaGlydata = PeakDistExt.get_alphaGlyData()
            self.__minValleydata = RefValley.get_x()
            '''QC CheckPeakFound '''
            if PeakDistExt.get_alphaGlyData()[0] != 0:
                outComes = DataAnalysis(DataExt.get_AlphaData()[1],DataExt.get_BetaData()[1],PeakDistExt.get_alphaGlyData()[2],DataExt.get_alphaMatrixData()[1],DataExt.get_betaMatrixData()[1], RefValley.get_x(),PeakDistExt.get_alphaGlyData()[1])
                self.__RatioCalaculationdata = [outComes.get_alphaRatio(),outComes.get_betaRatio(),outComes.get_glyAlphaRatio(),outComes.get_alphaMatrixRatio(),outComes.get_betaMatrixRatio(), outComes.get_oldglyAlphaRatio()]
                self.__ProbOutcomesdata = [outComes.get_alphaThalassemiaProb(),outComes.get_betaThalassemiaProb(),outComes.get_diabetesProb(), outComes.get_olddiabetesProb()]
                self.__resultString = outComes.get_strResult()
                self.__QcResult = "Pass"
            else:
                self.__RatioCalaculationdata = [None,None,None,None,None,None]
                self.__ProbOutcomesdata = [None,None,None,None]     
                self.__resultString = ["QcFail", "QcFail", "QcFail"]
                self.__QcResult = "HbA1C Fail"
        else:
            ''' Need to handle for when Alpha and Beta Not found'''
            self.__alphaGlydata = [0, 0, 0, 0]
            self.__RatioCalaculationdata = [None,None,None,None,None,None]
            self.__ProbOutcomesdata = [None,None,None,None]     
            self.__resultString = ["QcFail", "QcFail", "QcFail"]
            self.__QcResult = "QcFail"
            pass

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
