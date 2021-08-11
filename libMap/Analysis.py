import os
import scipy
from scipy.stats import norm
import csv
from libMap.PeakFinding import *
from libMap.Preprocessing import *
#import matplotlib.pyplot as plt
#from peakutils.plot import plot as pplot

class BestPeakEstimator():
    #Best peak estimate function
    def __init__(self, Mzml, Peakmz, PeakInt, Valleymz, ValleyInt,prom, widths):
        self.__alpha=self.set_Extract([0,100], Mzml, Peakmz, PeakInt, Valleymz, ValleyInt , prom, widths,noise =2.0)
        self.__beta=self.set_Extract([0,100], Mzml, Peakmz, PeakInt, Valleymz, ValleyInt , prom, widths,noise =2.0)
        if self.__alpha[0] != None and self.__beta[0] != None:
            self.__alphaMatrix = self.set_Extract([self.__alpha[0]+60,self.__alpha[0]+170], Mzml, Peakmz, PeakInt, Valleymz, ValleyInt , prom, widths,noise =1.0)
            self.__betaMatrix = self.set_Extract([self.__beta[0]+60,self.__beta[0]+150], Mzml, Peakmz, PeakInt, Valleymz, ValleyInt , prom, widths,noise =1.0)
        else:                                       
            self.__alphaMatrix = self.__alphaMatrix = [0, 0]
            self.__betaMatrix = self.__betaMatrix = [0, 0]

    def get_AlphaData(self):
        return self.__alpha

    def get_BetaData(self):
        return self.__beta

    '''Need A more accurate Region'''
    def get_alphaMatrixData(self):
        return self.__alphaMatrix

    '''Need A more accurate Region'''
    def get_betaMatrixData(self):
        return self.__betaMatrix

    def set_Extract(self, mzLim, mzdata, Pkmz, IPks, Vlmz, IVls, prom, widths, noise):
        peakmz = 0
        peakInt = 0
        SN = 0
        fwhm = 0
        promScale = 0
        for i, mz in enumerate(Pkmz):
            if mz >=mzLim[0] and mz<=mzLim[1] and prom[i] > promScale and IPks[i]>=noise:
                promScale = round(prom[i],3)
                peakmz = round(mz,3)
                peakInt = round(IPks[i],3)
                #SN = (IPks[i]/noise)
                fwhm = widths[i]
            else:
                pass
        return ([peakmz, peakInt, promScale, fwhm])

'''Need major optimization'''
class MinValleyEstimator():
    #Min peak valley estimator
    def __init__(self, alphaMz, Mzml, Peakmz, PeakInt, Valleymz, ValleyInt):
        if alphaMz[0] != 0:
            self.set_x([alphaMz[0]+20, alphaMz[0]+90], Mzml, Peakmz, Valleymz, PeakInt, ValleyInt)
        else:
            self.__MinValley = 0

    def get_x(self):
        return self.__MinValley

    def set_x(self, mzLim, mzdata, Pkmz, Vlmz, IPks, IVls):
        maxPk = 0
        minVal = "na"
        valpos = "na"
        mzlf = "na"
        mzrt= "na"
        regionlist =[]
        storedvalleyIntensity = 0
        storedvalleyposition = "na"
        self.__MinValley = [valpos, minVal]
        for i, valpt in enumerate(Vlmz):
            if valpt >= (mzLim[0]) and valpt < (mzLim[1]):
                regionlist.append(IVls[i])
        idealminvalley = min(regionlist)
        self.__MinValley = idealminvalley
        '''
        for i, valpt in enumerate(Vlmz):
            if valpt >= (mzLim[0]) and valpt < (mzLim[1]):
                if IVls[i] >  maxPk:
                    if IVls[i-1] == "na" or IVls[i+1] == "na":
                        pass
                    if IVls[i] < IVls[i-1] and IVls[i] < IVls[i+1]:
                        Ke ="na"
                        Kd ="na"
                        for j, peakpt in enumerate(Pkmz):
                            K1 = valpt-peakpt
                            K2 = peakpt-valpt
                            if peakpt >= mzLim[0] and peakpt < valpt and (0.5< K1 <25)  and IVls[i] < IPks[j]  :
                                Ke = K1
                                mzlf = peakpt
                                Ivalley1 = IVls[j]
                            if peakpt <= mzLim[1] and peakpt > valpt and (0.5< K2 <25) and IVls[i] < IPks[j] :
                                Kd = K2
                                mzrt = peakpt
                                Ivalley2 = IVls[j]
                            if mzrt != "na" and mzlf != "na":
                                mzrt = "na"
                                mzlf = "na"
                                if IVls[i] < storedvalleyIntensity:
                                    storedvalleyIntensity = IVls[i]
                                    storedvalleyposition = valpt
                                    valpos = storedvalleyposition
                                    minVal = storedvalleyIntensity
                                    self.__MinValley = [valpos, minVal]
                                if IVls[i] > storedvalleyIntensity:
                                    valpos = storedvalleyposition
                                    minVal = storedvalleyIntensity
                                    self.__MinValley = [valpos, minVal]
        '''

'''Need major optimization'''
class GlycatedEstimator():
    #Distpeakestimator
    def __init__(self, alphaData, Mzml, Peakmz, PeakInt, Valleymz, ValleyInt,prom, widths):
        #self.__GlyRegion = 83
        self.__alphaGlycated = self.set_Extract([alphaData[0]+80,alphaData[0]+85], Mzml, Peakmz, PeakInt, Valleymz, ValleyInt , prom, widths)

    def get_alphaGlyData(self):
        return self.__alphaGlycated

    def set_DataExtract(self,mzRef, Dist, Pkmz, IPks, Vlmz, IVls):
        maxPk1 = 0
        maxPk2 = 0
        mzPk = mzRef + Dist
        dPk = 5
        VAL = []
        Pkdetect = "na"
        self.__alphaGly = [Pkdetect, maxPk2]
        for k, mz in  enumerate(Vlmz):
            if mz > (mzPk - 50) and mz < (mzPk + 50):
                VAL.append(IVls[k])
        for j, I in enumerate(IPks):
            Signal = I - min(VAL)
            d = abs(Pkmz[j] - mzPk)
            if d < dPk:
                Pkdetect = round(Pkmz[j],3)
                dPk = d
                maxPk2 =round(I, 3)
                self.__alphaGly = [Pkdetect, maxPk2 ]
        if Pkdetect == "na":
            Pkdetect = mzPk
            maxPk2 = maxPk1
            self.__alphaGly = [Pkdetect, maxPk2 ]

    def set_Extract(self, mzLim, mzdata, Pkmz, IPks, Vlmz, IVls, prom, widths):
        peakmz = 0
        peakInt = 0
        SN = 0
        fwhm = 0
        promScale = 0
        for i, mz in enumerate(Pkmz):
            if mz >=mzLim[0] and mz<=mzLim[1] and prom[i] > promScale:
                promScale = round(prom[i],3)
                peakmz = round(mz,3)
                peakInt = round(IPks[i],3)
                #SN = (IPks[i]/noise)
                fwhm = widths[i]
            else:
                pass
        return ([peakmz, peakInt, promScale, fwhm])

'''Need to extract more haemoglobinopathy data from this class for haem tests'''
class Haemoglobinopathies():
    def __init__(self, alphaPeakMz, betaPeakMz, path,check):
        if alphaPeakMz[0] != "na" and betaPeakMz[0] != "na":
            self.set_HaeDist(alphaPeakMz, betaPeakMz)
            self.set_AlphaMutation(alphaPeakMz,path,check) #rawMz, peakMz, peakIntensity, valleyMz, valleyIntensity
            self.set_BetaMutation(betaPeakMz,path,check)
        else:
            self.__Dist = 0
            self.__AMutation = False
            self.__Aname = ""
            self.__BMutation =False
            self.__Bname = ""

    def get_HaeDist(self):
        return self.__Dist

    def get_AlphaMutation(self):
        return [self.__AMutation, self.__Aname]

    def get_BetaMutation(self):
        return [self.__BMutation, self.__Bname]

    def set_HaeDist(self,alphaPeakMz, betaPeakMz):
        self.__Dist = round(betaPeakMz[0] - alphaPeakMz[0], 3)

    def set_AlphaMutation(self, alphaPeak, path,check ): #rawMz, peakMz, peakIntensity, valleyMz, valleyIntensity
        if path.split(".")[-1] == "mzml":
           Decoder = DecodeMzml(path,alphaPeak[0]-50, alphaPeak[0]+50)
        else:
            Decoder = DecodeText(path,alphaPeak[0]-50, alphaPeak[0]+50)
        SmoothInt = Smoothing(Decoder.get_Int(), check, windowsize=5, cycle=3)
        NmIntensity = Normalise(SmoothInt.get_x())
        PeakDet = PeakDetection(NmIntensity.get_x(), Thhold=0.15, minimumDist=5)
        PeakExt = PeakExtraction(Decoder.get_mz(), NmIntensity.get_x(), PeakDet.get_Peaks() )
        ValleyExt = ValleyExtraction(Decoder.get_mz(),NmIntensity.get_x(), PeakDet.get_Valleys() )

        alphamutation = []
        self.__AMutation = False
        range = 99
        nl1 = 0
        threshold = 70
        maxvalue = "na"
        self.__Aname = ""
        mutation = "na"
        maxdmC = "na"
        Results = "na"
        #leftval = False
        #rightval = False
        counter = 0
        for i, mz in enumerate(PeakExt.get_PeakMzList()):
            leftval = False
            rightval = False
            for j, val in enumerate(ValleyExt.get_ValleyMzList()):
                #look to left of point
                if val >= (mz-0.5) and val <mz and ValleyExt.get_ValleyIntList()[j]*1.001 < PeakExt.get_PeakIntList()[i]:
                    leftval = True
                if val > mz and val <= (mz+0.9) and (PeakExt.get_PeakIntList()[i]-ValleyExt.get_ValleyIntList()[j]) >=0.021:
                    rightval = True
                if leftval==True and rightval==True:
                    leftval = False
                    rightval = False
                    alphamutation.append(mz - alphaPeak[0])
                else:
                    pass
        if len(alphamutation)>0:
            self.__AMutation = True
            with open(".\\resources\\Alpha_Haemoglobinopathy.csv") as csvfile:
                database = csv.reader(csvfile, delimiter =',')
                try:
                    while counter <= (len(alphamutation)-1) and (len(alphamutation)>0):
                        for row in database:
                            if nl1>0:
                                variance = (abs(float(alphamutation[counter])- float(row[5])) / range) * 100
                                Acc = 100 - variance
                                if (Acc > threshold):
                                    threshold = Acc     #float
                                    maxvalue = round(Acc, 3) #string
                                    mutation = row[0]     #string
                                    self.__Aname = row[3]   #string
                                    maxdmC = row[5]     #string
                                    Results = ("HB name = " + mutation + ", " + self.__Aname + "  | Dm/z(2+) = " + maxdmC + " | Acc = " + str(maxvalue) +"%\n")
                                elif (Acc == threshold):
                                    newResults = ("HB name = " + row[0] + ", " + row[3] + "  | Dm/z(2+) = " + row[5] + " | Acc = " + str(maxvalue) + "%\n")
                                    Results = Results + newResults
                                else:
                                    pass
                            nl1 += 1
                        counter += 1
                except ValueError:
                    print ("Error Opening Resource Alpha File")

    def set_BetaMutation(self, betaPeakMz, path, check ):
        #kjh
        if path.split(".")[-1] == "mzml":
           Decoder = DecodeMzml(path,betaPeakMz[0]-50, betaPeakMz[0]+50)
        else:
            Decoder = DecodeText(path,betaPeakMz[0]-50, betaPeakMz[0]+50)
        SmoothInt = Smoothing(Decoder.get_Int(), check, windowsize=5, cycle=3)
        NmIntensity = Normalise(SmoothInt.get_x())
        PeakDet = PeakDetection(NmIntensity.get_x(), Thhold=0.15, minimumDist=5)
        PeakExt = PeakExtraction(Decoder.get_mz(), NmIntensity.get_x(), PeakDet.get_Peaks() )
        ValleyExt = ValleyExtraction(Decoder.get_mz(),NmIntensity.get_x(), PeakDet.get_Valleys() )
        betamutation = []
        self.__BMutation = False
        range = 99
        nl1 = 0
        threshold = 70
        maxvalue = "na"
        self.__Bname = ""
        mutation = "na"
        maxdmC = "na"
        Results = "na"
        counter = 0
        for i, mz in enumerate(PeakExt.get_PeakMzList()):
                leftval = False
                rightval = False
                for j, val in enumerate(ValleyExt.get_ValleyMzList()):
                    if val >= (mz-0.5) and val <mz and ValleyExt.get_ValleyIntList()[j]*1.001 < PeakExt.get_PeakIntList()[i]:
                        leftval = True
                    if val > mz and val <= (mz+0.9) and (PeakExt.get_PeakIntList()[i]-ValleyExt.get_ValleyIntList()[j]) >=0.021:
                        rightval = True
                    if leftval==True and rightval==True:
                        leftval = False
                        rightval = False
                        betamutation.append(mz - betaPeakMz[0])
        if len(betamutation)>0:
            self.__BMutation = True
            with open(".\\resources\\Beta_Haemoglobinopathy.csv") as csvfile:
                database = csv.reader(csvfile, delimiter =',')
                try:
                    while counter <= (len(betamutation)-1) and (len(betamutation)>0):
                        for row in database:
                            if nl1>0:
                                variance = (abs(float(betamutation[counter])- float(row[5])) / range) * 100
                                Acc = 100 - variance
                                if (Acc > threshold):
                                    threshold = Acc     #float
                                    maxvalue = round(Acc, 3) #string
                                    mutation = row[0]     #string
                                    self.__Bname = row[3]   #string
                                    maxdmC = row[5]     #string
                                    Results = ("HB name = " + mutation + ", " + self.__Bname + "  | Dm/z(2+) = " + maxdmC + " | Acc = " + str(maxvalue) +"%\n")
                                elif (Acc == threshold):
                                    newResults = ("HB name = " + row[0] + ", " + row[3] + "  | Dm/z(2+) = " + row[5] + " | Acc = " + str(maxvalue) + "%\n")
                                    Results = Results + newResults
                                else:
                                    pass
                            nl1 += 1
                        counter += 1
                except ValueError:
                    print ("Error Opening Resource Beta File")

class DataAnalysis():
    def __init__(self, alpha, beta, alphaGlycated, alphaMatrix, betaMatrix, minValley, absGlycated):
        try:
            self.__AlphaRatio = self.set_alphaRatio(alpha)
        except:
            self.__AlphaRatio = None
        try:
            self.__BAratio = self.set_betaRatio(alpha, beta)
            self.__alphaThalassemiaProb = self.set_ProbOutcomes(self.__BAratio, 90 , 15 , 1, 0)
            self.__betaThalassemiaProb = self.set_ProbOutcomes(self.__BAratio, 51 , 25 , -1, 0)
        except:
            self.__BAratio = None
            self.__alphaThalassemiaProb = None
            self.__betaThalassemiaProb = None
        try:
            self.__GlyAratio = self.set_glyAlphaRatio(alpha,alphaGlycated)
            self.__diabetesProb = self.set_ProbOutcomes(self.__GlyAratio, 7 , 3 , -1 , 1)
        except:
            self.__GlyAratio = None
            self.__diabetesProb = None
        try:
            self.__MatrixA = self.set_alphaMatrixRatio(alpha,alphaMatrix)
        except:
            self.__MatrixA = None
        try:
            self.__MatrixB = self.set_betaMatrixRatio(alpha,betaMatrix)
        except:
            self.__MatrixB = None  
        try:
            self.__oldGlyAratio = self.set_glyAlphaRatio(alpha,(absGlycated-minValley))
            self.__oldDiabetesProb = self.set_ProbOutcomes(self.__oldGlyAratio, 7 , 3 , -1 , 1)
        except:
            self.__oldGlyAratio = None
            self.__oldDiabetesProb = None

        self.set_strResult(self.__alphaThalassemiaProb,self.__betaThalassemiaProb,self.__oldDiabetesProb)              

    def get_alphaThalassemiaProb(self):
        return self.__alphaThalassemiaProb
    def get_betaThalassemiaProb(self):
        return self.__betaThalassemiaProb
    def get_diabetesProb(self):
        return self.__diabetesProb
    def get_olddiabetesProb(self):
        return self.__oldDiabetesProb
    def get_alphaRatio(self):
        return self.__AlphaRatio
    def get_betaRatio(self):
        return self.__BAratio
    def get_glyAlphaRatio(self):
        return self.__GlyAratio   
    def get_oldglyAlphaRatio(self):
        return self.__oldGlyAratio
    def get_alphaMatrixRatio(self):
        return self.__MatrixA    
    def get_betaMatrixRatio(self):
        return self.__MatrixB
    def get_strResult(self):
        return self.__probResult
        
    def set_alphaRatio(self, alphaInt):
        AlphaRatio = round(float(alphaInt/1),3)
        return (AlphaRatio)      
    def set_betaRatio(self, alphaInt, betaInt):
        BAratio = round(float(betaInt)/alphaInt *100, 3)
        return (BAratio)
    def set_glyAlphaRatio(self, alphaInt, alGly):
        GlyAratio = round(float(alGly)/alphaInt *100, 3)
        return (GlyAratio)       
    def set_alphaMatrixRatio(self, alphaInt, alphaMatrix):
        MatrixA = round(float(alphaMatrix/1),3)
        return (MatrixA)     
    def set_betaMatrixRatio(self, alphaInt, betaMatrix):
        MatrixB = round(float(betaMatrix/1),3)
        return (MatrixB)

    def set_ProbOutcomes(self, value, mean, std, side, Type):
        Reference = scipy.stats.norm(mean, std).pdf(mean)
        if side == 0:
            if value > (mean-4*std) and value < (mean +4*std):
                probvalue = float(scipy.stats.norm(mean, std).pdf(value)) / Reference
            else:
                probvalue = 0.1
        elif side == -1:
            # Glycated alpha
            if value >= (mean -std) and value <= (mean+std):
                if Type ==0:
                    probvalue = float(scipy.stats.norm(mean, std).pdf(value)) / Reference
                else:
                    probvalue = float(scipy.stats.norm(mean, std).pdf(value)) / Reference
                    if value > mean:
                        probvalue = probvalue-0.6
                        return abs(1- probvalue)
                    elif value == mean:
                        probvalue = 0.5
                        return abs(1- probvalue)
                    else:
                        probvalue = (1-probvalue)+0.5
                        return abs(1- probvalue)
            elif value > (mean + std):
                if Type ==0:
                    probvalue = 0.9
                    return abs(1- probvalue)
                else:
                    probvalue = 0.0
                    return abs(1- probvalue)
            else: #value < (mean -std)
                if Type ==0:
                    probvalue = 0.0
                    return abs(1- probvalue)
                else:
                    probvalue = float(scipy.stats.norm(mean, std).pdf(value)) / Reference
                    return (round(probvalue,3))
        elif side == 1:
            if value >= mean and value <= (mean + 4*std):
                probvalue = float(scipy.stats.norm(mean, std).pdf(value)) / Reference
                return abs(1- probvalue)
            elif value > (mean + 4*std):
                probvalue = 0.0
                return abs(1- probvalue)
            else: #value < mean
                probvalue = 0.9
        else:
            probvalue = 1
            return abs(1- probvalue)

    def set_strResult(self, alphaTh, betaTh, diab):
        # Alpha Thalassemia
        self.__probResult = []
        if alphaTh != None:
            if alphaTh>=0.75:
               self.__probResult.append(True)
            elif alphaTh >0.5 and alphaTh <0.75:
                self.__probResult.append("Borderline")
            else:
                self.__probResult.append(False)
        else:
            self.__probResult.append("Fail")
        # Beta Thalassemia
        if betaTh != None:
            if betaTh>=0.75:
                self.__probResult.append(True)
            elif betaTh >0.5 and betaTh <0.75:
                self.__probResult.append("Borderline")
            else:
                self.__probResult.append(False)
        else:
            self.__probResult.append("Fail")
        # Pre-Diabetes
        if diab != None:
            if diab>=0.75:
                self.__probResult.append(True)
            elif diab >0.5 and diab <0.75:
                self.__probResult.append("Borderline")
            else:
                self.__probResult.append(False)
        else:
            self.__probResult.append("Fail")

class DataResults():
    def __init__(self, Ratios,Prob):
        self.__ratios = Ratios
        self.__prob = Prob
        self.__ratioResult = []
        self.__probResult = []

    def get_Ratioresult(self):
        return self.__ratioResult

    def get_Probresult(self):
        return self.__probResult

    def set_Probresult(self):
        # Alpha Thalassemia
        if self.__prob[1]>=0.75:
            print ("Prob Alpha Thalasemia Trait")
            self.__probResult.append(True)
        elif self.__prob[1] >0.5 and self.__prob[1] <0.75:
            print ("Prob Borderline Alpha Thalasemia Trait")
            self.__probResult.append("Borderline")
        else:
            print ("Prob indicates Alpha Thalasemia Normal")
            self.__probResult.append(False)
        # Beta Thalassemia
        if self.__prob[2]>=0.75:
            print ("Prob Beta Thalasemia Trait")
            self.__probResult.append(True)
        elif self.__prob[2] >0.5 and self.__prob[2] <0.75:
            print ("Prob Borderline Beta Thalasemia Trait")
            self.__probResult.append("Borderline")
        else:
            print ("Prob indicates Beta Thalasemia Normal")
            self.__probResult.append(False)
        # Pre-Diabetes
        if self.__prob[3]>=0.75:
            print ("Prob Diabetes Trait")
            self.__probResult.append(True)
        elif self.__prob[3] >0.5 and self.__prob[3] <0.75:
            print ("Prob Borderline Diabetes Trait")
            self.__probResult.append("Borderline")
        else:
            print ("Prob indicates Diabetes Normal")
            self.__probResult.append(False)

    def set_Ratioresult(self):
        # Alpha Thalassemia
        if self.__ratios[0] <= 20:
            print ("Ratio Alpha Thalasemia Trait")
            self.__ratioResult.append(True)
            #self.__ratioResult.append("Beta Peak Ratio at "+str(self.__ratios[0])+ " indicates Alpha Thalasemia.")
        # Beta Thalassemia
        elif self.__ratios[0] >= 90:
            print ("Beta Thalasemia Trait")
            self.__ratioResult.append(True)
            #self.__ratioResult.append("Beta Peak Ratio at "+str(self.__ratios[0])+ " indicates Beta Thalasemia.")
        else:
            print ("No Thalasemia Detected")
            self.__ratioResult.append(False)
            #self.__ratioResult.append("Normal.")
        # Pre-Diabetes
        if self.__ratios[1] >= 5 and self.__ratios[1] <9 :
            print ("Pre-Diabetes")
            self.__ratioResult.append(True)
        elif self.__ratios[1] >= 9:
            print ("Diabetes")
            self.__ratioResult.append(True)
        else:
            print ("Diabetes Not Detected")
            self.__ratioResult.append(False)
