from cx_Freeze import Executable
from cx_Freeze import setup as cx_setup
from distutils.core import setup
import sys
import os
import glob
import json
import scipy
#base = None
#if (sys.platform == "win32"):
    #base = "Win32GUI"

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

includefiles = ['AlgorithmSingle.cp37-win_amd64.pyd', 'Analysis.cp37-win_amd64.pyd', 'DTResult.cp37-win_amd64.pyd','Exporter.cp37-win_amd64.pyd','FileHandler.cp37-win_amd64.pyd', 'FolderHandler.cp37-win_amd64.pyd', 'MultipleWindow.cp37-win_amd64.pyd', 'MultipleWindowOutput.cp37-win_amd64.pyd', 'PeakFinding.cp37-win_amd64.pyd',
                'Preprocessing.cp37-win_amd64.pyd', 'SingleWindow.cp37-win_amd64.pyd', 'SingleWindowOutput.cp37-win_amd64.pyd', os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')]

includes = ['numpy.core._methods', 'numpy.lib.format','scipy','scipy.spatial.ckdtree','scipy.optimize', 'scipy.signal']
excludes = ['Tkconstants', 'Tkinter']
packages = ['numpy', 'os','scipy','scipy.optimize',]
path = []

GUI2Exe_Target_1 = Executable(script = "main.py", base = "Win32GUI", initScript = None, targetName = "MAP v-SCREEN.exe", icon = "C:/Users/christian.jardine.MAP/Documents/App_development/Covid-19/CovidPrototype/MAP_Vscreen_Version1/icons/Icon.ico")

#C:/Users/christian.jardine.MAP/Documents/App_development/BloodSoftware/MAP_Diagnostics_HBAnalyser2.1/FileExe/icons/Icon.ico

cx_setup(
version = "1.0.1",
description = "Covid-19 Gargle Saliva Analysis",
author = "cj_MAP I.P. Holders",
name = "MAP v-SCREEN",
options = {"build_exe": {"includes": includes,
"excludes": excludes,"packages": packages, "include_files": includefiles,
"path": path}}, executables = [GUI2Exe_Target_1],
 )
