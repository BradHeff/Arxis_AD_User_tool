from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("Functions", ["Functions.py"]),
    Extension("GUI", ["Gui.py"]),
    Extension("Main", ["Main.py"]),
    Extension("icons", ["icon.py"]),
]

setup(
    name="AADT",
    ext_modules=cythonize(ext_modules, language_level="3"),
)
