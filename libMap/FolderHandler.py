import sys
import os

class FolderAcceptance():
    def __init__(self, path):
        self.__Statusgreen ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid #39ff0d; background: #39ff0d;border-radius: 6px}"
        self.__Statusred ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid Red; background: Red;border-radius: 6px}"
        self.__Statusorange ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid orange; background: orange;border-radius: 6px}"
        self.__Statusyellow ="QCheckBox{background-color: transparent; margin:0em 5em 0em 5em}QCheckBox::indicator {border: 3px solid yellow; background: yellow;border-radius: 6px}"
        self.__count = 0
        self.set_x(path)

    def get_acceptance(self):
        return self.__acceptance

    def get_size(self):
        return self.__x

    def set_x(self, path):
        FILES = os.listdir(path)
        for filename in FILES:
            if filename.split(".")[-1] == "mzml" or filename.split(".")[-1] == "txt":
                self.__count +=1
            else:
                pass
        if self.__count >10:
            self.__x = self.__Statusgreen
            self.__acceptance = self.__Statusgreen
        elif self.__count >=5 and self.__count <=10:
            self.__x = self.__Statusorange
            self.__acceptance = self.__Statusgreen
        elif self.__count >=0 and self.__count <5:
            self.__x = self.__Statusyellow
            self.__acceptance = self.__Statusgreen
        else:
            self.__x = self.__Statusred
            self.__acceptance = self.__Statusred
