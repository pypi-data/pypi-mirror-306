import os
import sys
import pybind11
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

# 获取当前目录的父目录，以便找到 include 和 lib 目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ext_modules = [
    Pybind11Extension(
        'mxLogPy',
        ['pybind_wrapper.cpp'],
        include_dirs=[
            pybind11.get_include(),
            os.path.join(parent_dir, 'include')
        ],
        library_dirs=[
            os.path.join(parent_dir, 'lib')
        ],
        libraries=['mxLogLib'],
        language='c++',
        extra_compile_args=['-std=c++17'] if sys.platform != 'win32' else ['/std:c++17']
    ),
]

setup(
    name='mxLogPy',
    version='0.1.6',
    packages=find_packages(),
    package_data={
        'mxLogPy': ['*.pyd'],
    },
    include_package_data=True,
    install_requires=[
        'pybind11'
    ],
    description='High Performance and multiThread & async Log Library by C++',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='cmx',
    author_email='2507560089@qq.com',
    url='https://github.com/caomengxuan666/mxLog',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
