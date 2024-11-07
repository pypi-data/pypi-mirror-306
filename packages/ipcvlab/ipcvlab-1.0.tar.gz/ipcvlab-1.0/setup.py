from setuptools import setup, find_packages

setup(
    name='ipcvlab',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    package_data={'ipcvlab': ['*.ipynb', '*.py']},
)
