"""install library pip install -e . if in developer mode"""
from setuptools import setup, find_packages

setup(
    name="iris_insee_utils",
    version="0.0.1",
    url="https://github.com/mypackage.git",
    author="adrienpacifico",
    author_email="adrienpacificopro@gmail.com",
    description="get iris from gps points or address",
    packages=find_packages(),
    # install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)
