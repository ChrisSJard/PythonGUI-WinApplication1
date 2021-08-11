import os
class StatusHandler():
    def __init__(self, path):
        self.__Statusgreen ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid #39ff0d; background: #39ff0d;border-radius: 6px}"
        self.__Statusred ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid Red; background: Red;border-radius: 6px}"
        self.__Statusgrey ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid #7a7979; background: #7a7979;border-radius: 6px}"
        self.__x = self.__Statusgrey
        self.set_x(path)

    def get_x(self):
        return self.__x

    def set_x(self, x):
        if x.split(".")[-1] == "mzml" or x.split(".")[-1] == "txt":
            self.__x = self.__Statusgreen
        elif x == "...Specify File Location":
            self.__x = self.__Statusgrey
        else:
            self.__x = self.__Statusred

class SizeHandler():
    def __init__(self, path):
        self.__Statusgreen ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid #39ff0d; background: #39ff0d;border-radius: 6px}"
        self.__Statusred ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid Red; background: Red;border-radius: 6px}"
        self.__filesize = os.stat(path)
        self.__sizelimit = 13000000
        self.set_x()

    def get_x(self):
        return self.__x

    def set_x(self):
        if  self.__filesize.st_size >= self.__sizelimit :
            # Red Light
            self.__x = self.__Statusred
        else:
            #Green Light
            self.__x = self.__Statusgreen

class StatusDataExtraction():
    def __init__(self,path):
        self.__Statusgreen ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid #39ff0d; background: #39ff0d;border-radius: 6px}"
        self.__Statusred ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid Red; background: Red;border-radius: 6px}"
        self.__DataInfo = path.split("/")[-1]
        print ("path = ", self.__DataInfo)
        self.__count = 0
        self.set_x()

    def get_x(self):
        return self.__x

    def set_x(self):
        for i in self.__DataInfo.split("-"):
            self.__count += 1
        if self.__count >=3:
            id = self.__DataInfo.split("-")[0]
            # green light
            self.__x = self.__Statusgreen
        else:
            # red light
            self.__x = self.__Statusred
