import xlsxwriter
import datetime
from datetime import datetime
import csv
import os

def fileExtract(datafile):
    try:
        userID = datafile.split("-")[0]
    except Exception:
        userID = datafile
    try:
        machine = datafile.split("-")[6]
    except Exception:
        machine = "Unknown"
    try:
        location = datafile.split("-")[7]
    except Exception:
        location = "Unknown"
    try:
        date = datafile.split("-")[8]
    except Exception:
        now = datetime.now()
        date = now.strftime('%d-%m-%Y_%H_%M_%S')
    try:
        test = datafile.split("-")[5]
    except Exception:
        test = "Diabetes"
    try:
        sampleType = datafile.split("-")[4]
    except Exception:
        sampleType = "Unknown"
    try:
        matrix = datafile.split("-")[3]
    except Exception:
        matrix = "Unknown"
    try:
        dilution = datafile.split("-")[2]
    except Exception:
        dilution = "Unknown"
    try:
        repeats = datafile.split("-")[1]
    except Exception:
        repeats = "Unknown"
    return ([userID, machine, location, date, test, sampleType, matrix, dilution, repeats])

def csvExport(filename, Hbresult,QcResult,HbA1cRegion,HbA1cReading,HbA1cRatio, HbA1cAbsolute, HbA1cProbability, oldHbA1cRatio, oldHbA1cProb, AlphaPeak ):
    now = datetime.now()
    dt_string = now.strftime('%d-%m-%Y_%H_%M_%S')
    savelocation = os.path.dirname(os.path.realpath(filename))
    dir_loc = savelocation.replace(os.sep, '/')
    try:
        os.makedirs(savelocation + '\OutputResults')
    except FileExistsError:
        exist = ("Directory " , 'PDFReportFolder' ,  " already exists")
    datafile = (filename.split("/")[-1]).split(".")[0]
    datafileExtract = fileExtract(datafile)
    FolderOutput = dir_loc +"/OutputResults/"+datafile+"-Run-"+dt_string+"-result.csv"
    with open(FolderOutput, 'a', newline='') as file:
        thewriter = csv.writer(file)
        thewriter.writerow(["User ID", "Machine", "Location", "Date", "Test", "SampleType", 
                            "Matrix", "Dilution", "Repeat", "Result","Quality Control Reading",
                            "HbA1C Region","HbA1C Reading","HbA1C Ratio","HbA1C Absolute",
                            "HbA1C Probability", "HbA1C Previous Ratio", "HbA1C Previous Probability",
                            "Alpha Reading"
                           ])
        thewriter.writerow([datafileExtract[0],
                            datafileExtract[1],
                            datafileExtract[2],  
                            datafileExtract[3],
                            datafileExtract[4],
                            datafileExtract[5], 
                            datafileExtract[6], 
                            datafileExtract[7], 
                            datafileExtract[8],
                            Hbresult, QcResult, HbA1cRegion,HbA1cReading,HbA1cRatio, HbA1cAbsolute, HbA1cProbability,oldHbA1cRatio, oldHbA1cProb, AlphaPeak,
                          ])
        #----------------------------------------------------------------------------------------------------------------------------------------
    file.close()

def Sheet1(workbook, header,filenameList,outcome, prom, ratio, probability, absolute,oldRatio, oldProb, alphaPeak):
    #------------------------------------------------------------------------------------------------------------------------------------
    #Signal to Noise Data Sheet
    worksheet = workbook.add_worksheet('Prom Readings')
    # Widen the first column to make the text clearer
    worksheet.set_column('A:A', 20)
    # Add a bold format to use to highlight cells
    bold = workbook.add_format({'bold': True})
    # Write Header text.
    count = 0
    hcol = 0
    hrow = 0
    for i in header:
        worksheet.write(hrow,hcol,i, bold)
        hcol+=1
    # Write Int data text
    row = 1
    for i in range(len(filenameList)):
        worksheet.write(row, 0, filenameList[i])  # filename
        worksheet.write(row, 1, outcome[i])  
        worksheet.write(row, 2, prom[i]) 
        worksheet.write(row, 3, ratio[i])
        worksheet.write(row, 4, probability[i])
        worksheet.write(row, 5, absolute[i])
        worksheet.write(row, 6, oldRatio[i])
        worksheet.write(row, 7, oldProb[i])
        worksheet.write(row, 8, alphaPeak[i])
        row+=1

def excelExport(savelocation,filenameList,outcome, prom, ratio, probability, absolute, oldRatio, oldProb, alphaPeak ):
    #create a new excel file and add worksheet.
    now = datetime.now()
    dt_string = now.strftime('%d-%m-%Y_%H_%M_%S')
    dir_loc = savelocation.replace('/',os.sep)
    try:
        os.makedirs(dir_loc + '\OutputResults')
    except FileExistsError:
        exist = ("Directory " , 'PDFReportFolder' ,  " already exists")
    loc = savelocation +"/OutputResults/MAPHB_Data_run-"+dt_string+".xlsx"
    workbook = xlsxwriter.Workbook(loc)
    header = ['Filename', 'Diabetes Outcome', 'HbA1c Prom', 'HbA1c Ratio', 'HbA1c Probability','HbA1c Absolute Int','HbA1c Old Ratio', 'HbA1c Old Probability', 'AlphaPeak']
    Sheet1(workbook,header,filenameList, outcome, prom, ratio, probability, absolute,oldRatio, oldProb, alphaPeak)
    workbook.close()