# -*- coding: utf-8 -*-
# @Project: auto_test
# @Description: 
# @Time   : 2024-07-29 上午10:52
# @Author : 毛鹏
import os

from Cython.Build import cythonize
from setuptools import setup

current_directory = os.path.abspath(__file__)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))
setup(
    ext_modules=cythonize(fr"{root_dir}\mangokit\mango\mango.pyx")
)

# python D:\GitCode\MangoKit\mangokit\mango\setup.py build_ext --inplace
