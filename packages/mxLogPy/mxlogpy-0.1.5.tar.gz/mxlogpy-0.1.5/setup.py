from setuptools import setup, find_packages

setup(
    name='mxLogPy',
    version='0.1.5',
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
