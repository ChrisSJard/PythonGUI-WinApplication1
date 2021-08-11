from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("AlgorithmSingle",  ["AlgorithmSingle.py"]),
    Extension("Analysis",  ["Analysis.py"]),
    Extension("Exporter", ["Exporter.py"]),
    Extension("FileHandler",  ["FileHandler.py"]),
    Extension("FolderHandler",  ["FolderHandler.py"]),
    Extension("MultipleWindow",  ["MultipleWindow.py"]),
    Extension("MultipleWindowOutput",  ["MultipleWindowOutput.py"]),
    Extension("PeakFinding",  ["PeakFinding.py"]),
    Extension("Preprocessing",  ["Preprocessing.py"]),
    Extension("SingleWindow",  ["SingleWindow.py"]),
    Extension("SingleWindowOutput",  ["SingleWindowOutput.py"])
#   ... all your modules that need be compiled ...
]
setup(
    name = 'Application MAP HB',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
